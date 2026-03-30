"""
BasePage: 基础页面对象类
封装 Selenium 常用操作和公共方法
"""
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """页面对象基类"""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
        self.poll_frequency = 0.5

    def find_element(self, locator, timeout=None):
        """
        查找单个元素
        :param locator: 元组 (By.XXX, "value")
        :param timeout: 超时时间
        :return: WebElement
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(
                self.driver, timeout, self.poll_frequency
            ).until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            raise NoSuchElementException(f"元素未找到: {locator}")

    def find_elements(self, locator, timeout=None):
        """查找多个元素"""
        timeout = timeout or self.timeout
        try:
            elements = WebDriverWait(
                self.driver, timeout, self.poll_frequency
            ).until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            return []

    def click(self, locator, timeout=None):
        """点击元素"""
        element = self.find_element(locator, timeout)
        element.click()
        return element

    def input_text(self, locator, text, timeout=None):
        """输入文本"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator, timeout=None):
        """获取元素文本"""
        element = self.find_element(locator, timeout)
        return element.text

    def get_attribute(self, locator, attr_name, timeout=None):
        """获取元素属性"""
        element = self.find_element(locator, timeout)
        return element.get_attribute(attr_name)

    def is_element_visible(self, locator, timeout=None):
        """元素是否可见"""
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, locator, timeout=None):
        """元素是否可点击"""
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_alert(self, timeout=None):
        """等待 alert 弹窗出现"""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout, self.poll_frequency).until(
            EC.alert_is_present()
        )

    def accept_alert(self):
        """接受 alert"""
        alert = self.wait_for_alert()
        alert.accept()

    def switch_to_frame(self, locator):
        """切换到 iframe"""
        if isinstance(locator, str):
            self.driver.switch_to.frame(locator)
        else:
            frame = self.find_element(locator)
            self.driver.switch_to.frame(frame)

    def switch_to_default_content(self):
        """切回主文档"""
        self.driver.switch_to.default_content()

    def scroll_into_view(self, locator):
        """滚动到元素可见"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)

    def get_current_url(self):
        """获取当前 URL"""
        return self.driver.current_url

    def screenshot(self, name):
        """截图"""
        self.driver.save_screenshot(f"./screenshots/{name}.png")
