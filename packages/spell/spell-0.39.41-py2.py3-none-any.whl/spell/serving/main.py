import multiprocessing
from typing import Optional

from hypercorn.config import Config as HypercornConfig
from hypercorn.run import run as hypercorn_run


def run_proxy() -> None:
    from spell.serving.proxy import server_conf

    config = HypercornConfig.from_object(server_conf)
    config.application_path = "spell.serving.proxy.app:app"
    hypercorn_run(config)


def run_servers(is_batching_enabled: bool, num_workers: Optional[int]) -> None:
    from spell.serving import server_conf

    config = HypercornConfig.from_object(server_conf)
    if num_workers:
        config.workers = num_workers
    if is_batching_enabled:
        config.bind = "localhost:5000"
    config.application_path = "spell.serving.app:app"
    hypercorn_run(config)


def main(is_batching_enabled, num_server_workers):
    if is_batching_enabled:
        proxy_process = multiprocessing.Process(target=run_proxy, daemon=True)
        proxy_process.start()
    run_servers(is_batching_enabled, num_server_workers)
