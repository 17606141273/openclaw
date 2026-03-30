"""
Tab Page Object
标签页测试页面
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class TabPage(BasePage):
    """标签页测试页面"""
    
    TAB_HOME = (By.XPATH, "//button[@class='tab' and contains(text(), '首页')]")
    TAB_PRODUCT = (By.XPATH, "//button[@class='tab' and contains(text(), '产品')]")
    TAB_ABOUT = (By.XPATH, "//button[@class='tab' and contains(text(), '关于')]")
    
    TAB_CONTENT_HOME = (By.ID, "tab1")
    TAB_CONTENT_PRODUCT = (By.ID, "tab2")
    TAB_CONTENT_ABOUT = (By.ID, "tab3")
    
    def switch_to_home(self):
        """切换到首页"""
        self.click(self.TAB_HOME)
    
    def switch_to_product(self):
        """切换到产品页"""
        self.click(self.TAB_PRODUCT)
    
    def switch_to_about(self):
        """切换到关于页"""
        self.click(self.TAB_ABOUT)
    
    def is_tab_active(self, tab_name):
        """判断标签页是否激活"""
        tab_map = {
            "home": self.TAB_HOME,
            "product": self.TAB_PRODUCT,
            "about": self.TAB_ABOUT
        }
        tab = self.find_element(tab_map.get(tab_name))
        return "active" in tab.get_attribute("class")
    
    def is_content_visible(self, content_name):
        """判断内容是否可见"""
        content_map = {
            "home": self.TAB_CONTENT_HOME,
            "product": self.TAB_CONTENT_PRODUCT,
            "about": self.TAB_CONTENT_ABOUT
        }
        content = self.find_element(content_map.get(content_name))
        return content.is_displayed() and "active" in content.get_attribute("class")
    
    def get_tab_content_text(self, content_name):
        """获取标签页内容文本"""
        content_map = {
            "home": self.TAB_CONTENT_HOME,
            "product": self.TAB_CONTENT_PRODUCT,
            "about": self.TAB_CONTENT_ABOUT
        }
        return self.get_text(content_map.get(content_name))
