from pathlib import Path

from starlette.config import Config

config = Config("/config/.env")

# Host and port the model server is running on
MODEL_SERVER_HOST = config("MODEL_SERVER_HOST", default="0.0.0.0")
MODEL_SERVER_PORT = config("MODEL_SERVER_PORT", cast=int, default=5000)
# Maximum size a batch is allowed to be
MAX_BATCH_SIZE = config("MAX_BATCH_SIZE", cast=int, default=100)
# Maximum time to wait before processing a request
REQUEST_TIMEOUT_MS = config("REQUEST_TIMEOUT_MS", cast=int, default=500)
# Path to the Python module containing predictor"
MODULE_PATH = config("MODULE_PATH", cast=Path, default=None)
# Python path to the module containing the predictor"
PYTHON_PATH = config("PYTHON_PATH", default=None)
# Path to the module containing the predictor
ENTRYPOINT = config("ENTRYPOINT", cast=Path, default=None)
# Run the proxy server in debug mode
DEBUG = config("DEBUG", cast=bool, default=False)
