import os
import threading
import urllib.parse

import pytest
import selenium
import selenium.webdriver
import selenium.webdriver.remote.webdriver
import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient
from selenium.webdriver.remote.webdriver import WebDriver
from testcontainers.selenium import BrowserWebDriverContainer

from src.main import create_app


@pytest.fixture()
def app():
    return create_app()


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def background_app_port() -> int:
    app = create_app()
    port = 9000

    server_has_started = threading.Event()

    background_thread = threading.Thread(
        target=_run_background_app,
        args=[app, port, server_has_started],
        daemon=True,
        name="Uvicorn Background Thread",
    )

    background_thread.start()
    server_has_started.wait()

    return port


def _run_background_app(app: FastAPI, port: int, server_has_started: threading.Event):
    server_has_started.set()

    uvicorn.run(app, port=port)


class Browser:
    def __init__(self, base_url: str, driver: WebDriver):
        self._base_url = base_url

        self.driver = driver
        driver.maximize_window()

    def navigate_to(self, path: str):
        url = urllib.parse.urljoin(self._base_url, path)

        self.driver.get(url)


@pytest.fixture(scope="session")
def browser(background_app_port: int):
    external_chrome_url = os.environ.get("TEST_CHROME_URL")

    if external_chrome_url is None:
        chrome = BrowserWebDriverContainer(
            selenium.webdriver.DesiredCapabilities.CHROME,
            image="selenium/standalone-chrome:latest",
        )

        with chrome:
            driver = chrome.get_driver()
            browser = Browser(
                base_url=f"http://host.docker.internal:{background_app_port}",
                driver=driver,
            )

            yield browser

            driver.quit()
    else:
        driver = selenium.webdriver.Remote(
            command_executor=external_chrome_url,
        )
        try:
            browser = Browser(
                # During CI, connect to localhost
                base_url=f"http://localhost:{background_app_port}",
                driver=driver,
            )

            yield browser
        finally:
            driver.quit()
