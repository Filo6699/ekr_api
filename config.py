import os
from decouple import config as env

bind = "127.0.0.1:8001"

# Manually set amount of workers
workers = 1
# Set the number of workers based on server capabilities
# workers = os.cpu_count() * 2 + 1

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"  # Set the log level (debug, info, warning, error, critical)

# Worker settings
worker_class = "uvicorn.workers.UvicornWorker"  # Use the Uvicorn worker class

MAX_REQUEST_LINE_SIZE = 4094
MAX_REQUEST_FIELDS = 100
MAX_REQUEST_FIELD_SIZE = 8190

# Security settings
limit_request_line = MAX_REQUEST_LINE_SIZE
limit_request_fields = MAX_REQUEST_FIELDS
limit_request_field_size = MAX_REQUEST_FIELD_SIZE

if env("SSL") == "on":
    keyfile = env("SSL_PRIVATE_KEY_PATH")
    certfile = env("SSL_CERTIFICATE_PATH")
