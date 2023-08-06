import asyncio
from collections.abc import Sequence
import pickle
from typing import Any, Awaitable, Callable, Iterable, List, Optional, Tuple

from httpx import (
    AsyncClient,
    HTTPStatusError,
    Request as HttpxRequest,
    Response as HttpxResponse,
)
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route

from spell.serving.exceptions import InvalidServerConfiguration
from spell.serving.proxy import settings
from spell.serving.responses import httpx_response_to_starlette, wrap_response
from spell.serving.types import (
    PredictorResponse,
    ProxyPredictCallback,
    ProxyPredictCallbackResponse,
)
from spell.serving.utils import import_from_entrypoint, import_user_module, retry


class BatchProcessingError(Exception):
    def __init__(self, result: Any):
        self.result = result

    @classmethod
    def from_response(cls, response: HttpxResponse):
        try:
            content = pickle.loads(response.content)
        except (KeyError, pickle.PickleError):
            return cls(httpx_response_to_starlette(response))
        if isinstance(content, Response):
            return cls(content)
        return cls(httpx_response_to_starlette(response))


class BatchDispatcher:
    """This class wraps a function which accepts batches, batches incoming requests, then calls the
    function with those batches

    When a request comes into handle_request, it starts a new timeout task if none is running. It
    then creates a future for the request and pushes both the future and the request onto a queue
    and awaits the future's result. If the queue has exceeded its maximum size, it creates a batch
    and cancels the timeout task. It then calls the callback with the batch. This callback returns
    a list of results, one per request, and therefore one per future. It then assigns the futures
    the appropriate result. A timeout task creates a batch from whatever requests are in the queue.
    """

    class _InitialTimeoutTask:
        # This is a dummy task which is already marked as done. Only used for initial request.
        # It's so we don't have to do a none check on every request when it's only necessary
        # for the very first request
        def done(self):
            return True

        def cancel(self):
            pass

    __slots__ = [
        "max_batch_size",
        "timeout_ms",
        "callback",
        "requests_queue",
        "futures_queue",
        "_timeout_task",
        "_loop",
    ]

    def __init__(self, max_batch_size: int, timeout_ms: int) -> None:
        self.max_batch_size = max_batch_size
        self.timeout_ms = timeout_ms
        self.requests_queue = []
        self.futures_queue = []
        self._timeout_task = self._InitialTimeoutTask()

        # These syncronization primitives must be created after an async loop is avaialble
        # This async loop is created after Starlette is initialized
        self._loop = None

        # This callback is set when the class is used as a decorator
        self.callback = None

    @classmethod
    def from_settings(cls):
        return cls(settings.MAX_BATCH_SIZE, settings.REQUEST_TIMEOUT_MS)

    def initialize_async_primitives(self, loop: Optional[asyncio.BaseEventLoop] = None) -> None:
        self._loop = loop if loop else asyncio.get_event_loop()

    def __call__(self, func: ProxyPredictCallback) -> Callable[[Any], Awaitable[PredictorResponse]]:
        self.callback = func
        return self.handle_request

    async def handle_request(self, request: Any) -> asyncio.Future:
        # The data in this request is fully arbitrary so long as self.callback can accept a list
        # of it.
        # If no timer is running, start one
        future = self._loop.create_future()
        self.requests_queue.append(request)
        self.futures_queue.append(future)

        if self._timeout_task.done():
            self._timeout_task = self._loop.create_task(self.schedule_timeout())
        if len(self.requests_queue) >= self.max_batch_size:
            batch, futures = self.make_batch()
            await self.execute_batch(batch, futures)
        return await future

    async def schedule_timeout(self) -> None:
        try:
            await asyncio.sleep(self.timeout_ms / 1000)
            batch, futures = self.make_batch()
            await self.execute_batch(batch, futures)
        except asyncio.CancelledError:
            pass

    def make_batch(self) -> Tuple[List[asyncio.Future], List[Any]]:
        # self._timeout_task.cancel()
        batch = self.requests_queue
        futures = self.futures_queue
        self.requests_queue = []
        self.futures_queue = []
        return batch, futures

    async def execute_batch(self, batch: List[Any], futures: List[asyncio.Future]) -> None:
        done = False
        try:
            responses = await self.callback(batch)
            self.set_futures_to_responses(futures, responses, expected_length=len(batch))
            done = True
        # This would happen if Starlette cancels this task (on server shutdown)
        except asyncio.CancelledError:
            pass  # rely on the finally block to cancel all futures
        except BatchProcessingError as e:
            self.set_all_futures_to_value(futures, e.result)
            done = True
        except Exception as e:
            for future in futures:
                if not future.done():
                    future.set_result(e)
            done = True
        finally:
            if not done:
                for future in futures:
                    if not future.done():
                        # This returns a 0-length 500 status response to the user
                        future.cancel()

    def set_futures_to_responses(
        self, futures: List[asyncio.Future], responses: List[Any], expected_length: int
    ) -> None:
        # It is possible that a user returned something which isn't list-like from
        # their predict. We check that here
        if not isinstance(responses, Sequence):
            msg = "Batch predict resonses must be iterable and support len()"
            self.set_user_error_responses(futures, msg)
        elif len(responses) != expected_length:
            msg = f"Response length mismatch! Expected {expected_length}, but got {len(responses)}"
            self.set_user_error_responses(futures, msg)
        else:
            for future, response in zip(futures, responses):
                future.set_result(response)

    @staticmethod
    def set_user_error_responses(futures: Iterable[asyncio.Future], error_msg: str) -> None:
        print(f"ERROR: {error_msg}")
        BatchDispatcher.set_all_futures_to_value(
            futures, PlainTextResponse(error_msg, status_code=500)
        )

    @staticmethod
    def set_all_futures_to_value(futures: List[asyncio.Future], value: Any) -> None:
        for future in futures:
            future.set_result(value)

    def reset(self):
        # This is only used for testing
        self._timeout_task.cancel()
        while self.futures_queue:
            future = self.futures_queue.pop()
            future.cancel()


class Proxy:
    __slots__ = [
        "client",
        "_base_url",
        "dispatcher",
        "_dispatch_predict",
        "_semaphore",
    ]

    def __init__(
        self,
        client: AsyncClient,
        dispatcher: BatchDispatcher,
        outbound_host: str,
        outbound_port: int,
    ) -> None:
        self.client = client
        self._base_url = f"http://{outbound_host}:{outbound_port}"
        self.dispatcher = dispatcher
        self._dispatch_predict = self.dispatcher(self._do_predict)

    def initialize_async_primitives(self, loop: Optional[asyncio.BaseEventLoop] = None) -> None:
        self.dispatcher.initialize_async_primitives(loop=loop)

    @classmethod
    def from_settings(cls, client: AsyncClient, dispatcher: BatchDispatcher):
        # While we aren't running any user code directly, because we are unpickling objects from user
        # code, we could attempt to unpickle a user-defined data type. This would cause an import
        # error if we don't load their module. This also ensures that any third-party data structures
        # returned by /prepare are in our runtime.
        if settings.ENTRYPOINT is not None:
            import_from_entrypoint(settings.ENTRYPOINT)
        else:
            if not (settings.MODULE_PATH and settings.PYTHON_PATH):
                raise InvalidServerConfiguration(
                    "Either Module path and Python path must be specified or entrypoint must be specified"
                )
            if not settings.MODULE_PATH.is_dir():
                raise InvalidServerConfiguration("Module path must be a directory")

            import_user_module(module_path=settings.MODULE_PATH, python_path=settings.PYTHON_PATH)
        return cls(
            client=client,
            dispatcher=dispatcher,
            outbound_host=settings.MODEL_SERVER_HOST,
            outbound_port=settings.MODEL_SERVER_PORT,
        )

    async def passthrough(self, request: Request) -> Response:
        """This method handles all requests except those to /predict and passes them directly to
        the model server"""
        body = await request.body()
        headers = dict(request.headers)
        url = self._get_full_url(request.url.path, request)

        @retry(request.url.path)
        async def call():
            async with self.client as c:
                response = await c.send(
                    HttpxRequest(
                        request.method,
                        url,
                        headers=headers,
                        content=body,
                    )
                )

            return httpx_response_to_starlette(response)

        return await call()

    async def predict(self, request: Request) -> Response:
        body = await request.body()
        headers = dict(request.headers)
        prepare_url = self._get_full_url("/prepare", request)

        @retry(request.url.path)
        async def call_prepare():
            async with self.client as c:
                response = await c.post(prepare_url, headers=headers, content=body)
            response.raise_for_status()
            return pickle.loads(response.content)

        try:
            prepared_response = await call_prepare()
        except HTTPStatusError as e:
            return httpx_response_to_starlette(e.response)
        resp = await self._dispatch_predict(prepared_response)
        # This will handle exceptions thrown in dispatcher
        if isinstance(resp, Exception):
            raise resp
        # Here we use wrapped response because the result of the /predict method
        # is any pickleable type supported by wrap_response
        ret = await wrap_response(resp)
        return ret

    async def _do_predict(self, data: List[Any]) -> ProxyPredictCallbackResponse:
        data_content = pickle.dumps(data)
        predict_url = f"{self._base_url}/predict"

        @retry("/predict")
        async def call_predict():
            async with self.client as c:
                response = await c.post(
                    predict_url,
                    headers={
                        "Content-Type": "application/octet-stream",
                    },
                    content=data_content,
                )
            response.raise_for_status()
            return pickle.loads(response.content)

        try:
            return await call_predict()
        except HTTPStatusError as e:
            raise BatchProcessingError.from_response(e.response)

    def _get_full_url(self, endpoint: str, request: Request) -> str:
        url = f"{self._base_url}{endpoint}"
        # Micro-optimization. query params impl is a mapping in which len() is faster than str()
        # which does url-encoding
        if len(request.query_params) > 0:
            url += f"?{str(request.query_params)}"
        return url

    def get_routes(self) -> List[Route]:
        return [
            Route("/predict", self.predict, methods=["POST"]),
            Route("/{path:path}", self.passthrough),
        ]


def make_app(proxy: Optional[Proxy] = None) -> Starlette:
    if not proxy:
        dispatcher = BatchDispatcher.from_settings()
        proxy = Proxy.from_settings(AsyncClient(), dispatcher)
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        ),
        Middleware(GZipMiddleware),
    ]
    return Starlette(
        debug=settings.DEBUG,
        routes=proxy.get_routes(),
        middleware=middleware,
        on_startup=[proxy.initialize_async_primitives],
    )
