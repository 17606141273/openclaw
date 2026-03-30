"""
Base Page Object
所有页面的基类，封装通用方法
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    """基础页面类，封装通用方法"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
    
    def open(self, url):
        """打开网页"""
        self.driver.get(url)
    
    def find_element(self, locator):
        """查找元素"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """查找多个元素"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click(self, locator):
        """点击元素"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys(self, locator, text):
        """输入文本"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """获取元素文本"""
        return self.find_element(locator).text
    
    def is_element_visible(self, locator):
        """判断元素是否可见"""
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False
    
    def wait_for_alert(self):
        """等待提示消息出现"""
        return self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
        )
    
    def scroll_to_element(self, locator):
        """滚动到元素"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    
    def take_screenshot(self, filename):
        """截图"""
        self.driver.save_screenshot(filename)
