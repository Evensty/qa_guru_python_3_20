import allure
import pytest
from selene.support.shared import browser
from appium import webdriver
from appium.options.android import UiAutomator2Options
import os
from dotenv import load_dotenv

from mobile_tests.utils import attach


@pytest.fixture(scope="function", autouse=True)
def driver_config():
    load_dotenv()
    options = UiAutomator2Options().load_capabilities(
        {
            "platformName": "android",
            "platformVersion": "9.0",
            "deviceName": "Google Pixel 3",
            "app": os.getenv("app"),
            "bstack:options": {
                "projectName": os.getenv("projectName"),
                "buildName": os.getenv("buildName"),
                "sessionName": os.getenv("sessionName"),
                "userName": os.getenv("browserstack.userName"),
                "accessKey": os.getenv("browserstack.accessKey"),
            },
        }
    )

    with allure.step("setup driver"):
        browser.config.driver = webdriver.Remote(
            os.getenv("remote_url"), options=options
        )

    yield
    attach.add_video(browser)
    browser.quit()
