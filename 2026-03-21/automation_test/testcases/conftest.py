"""
conftest.py: pytest 配置和 fixture
"""
import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def browser():
    """
    浏览器 fixture
    session 级别：整个测试会话只启动一次浏览器
    """
    options = Options()
    options.add_argument("--start-maximized")
    # 取消自动化提示
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def home_page(browser):
    """
    首页 fixture
    function 级别：每个测试函数都会重新打开页面
    """
    from pages.home_page import HomePage
    page = HomePage(browser)
    yield page


@pytest.fixture(scope="session", autouse=True)
def setup_screenshots_dir():
    """
    自动创建截图目录
    """
    os.makedirs("./screenshots", exist_ok=True)
    os.makedirs("./screenshots/failed", exist_ok=True)
    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    失败自动截图的钩子
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = None
        if "browser" in item.funcargs:
            driver = item.funcargs["browser"]
        elif "home_page" in item.funcargs:
            driver = item.funcargs["home_page"].driver

        if driver:
            screenshot_dir = "./screenshots/failed"
            screenshot_name = f"{item.name}_{int(time.time())}.png"
            driver.save_screenshot(os.path.join(screenshot_dir, screenshot_name))
