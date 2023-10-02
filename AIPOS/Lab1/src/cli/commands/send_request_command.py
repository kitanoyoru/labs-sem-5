import asyncio
import logging

import click
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = httpx.AsyncClient()


async def main(method: str, path: str):
    client.send
    response = await client.request(
        method=method,
        url=f"http://localhost:8000/api/v0/{path}",
    )

    logger.info(f"<{response.status_code}> Request results: {response.text}")


@click.command()
@click.option("--method", default="GET", help="Specify request method")
@click.option("--file", default="test.html", help="Specify file path")
def send_request(method: str, path: str):
    asyncio.run(main(method, path))
