import logging
import os

from src.cli import cli

log_file = os.environ["LOG_FILE"]
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    encoding="UTF-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

cli()
