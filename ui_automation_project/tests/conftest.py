"""
Pytest Configuration
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages import *
from utils import DriverFactory


@pytest.fixture(scope="function")
def driver():
    """创建浏览器驱动"""
    driver = DriverFactory.create_driver(headless=True, browser="chrome")
    driver.get(DriverFactory.get_test_page_url())
    yield driver
    driver.quit()


@pytest.fixture
def form_page(driver):
    """表单页面对象"""
    return FormPage(driver)


@pytest.fixture
def button_page(driver):
    """按钮页面对象"""
    return ButtonPage(driver)


@pytest.fixture
def progress_page(driver):
    """进度条页面对象"""
    return ProgressPage(driver)


@pytest.fixture
def tab_page(driver):
    """标签页页面对象"""
    return TabPage(driver)


@pytest.fixture
def table_page(driver):
    """表格页面对象"""
    return TablePage(driver)


@pytest.fixture
def file_upload_page(driver):
    """文件上传页面对象"""
    return FileUploadPage(driver)
