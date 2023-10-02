import logging
import os

from .cli import cli

log_file = os.environ["LOG_FILE"]
logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

cli()
