"""
Button Page Object
按钮测试页面
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
import time


class ButtonPage(BasePage):
    """按钮测试页面"""
    
    PRIMARY_BUTTON = (By.XPATH, "//button[contains(text(), '主要按钮')]")
    SUCCESS_BUTTON = (By.XPATH, "//button[contains(text(), '成功按钮')]")
    DANGER_BUTTON = (By.XPATH, "//button[contains(text(), '危险按钮')]")
    WARNING_BUTTON = (By.XPATH, "//button[contains(text(), '警告按钮')]")
    MODAL_BUTTON = (By.XPATH, "//button[contains(text(), '打开弹窗')]")
    LOADING_BUTTON = (By.XPATH, "//button[contains(text(), '显示加载')]")
    
    MODAL = (By.ID, "modal")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//div[@id='modal']//button[contains(text(), '关闭')]")
    LOADER = (By.ID, "loader")
    
    def click_primary_button(self):
        """点击主要按钮"""
        self.click(self.PRIMARY_BUTTON)
    
    def click_success_button(self):
        """点击成功按钮"""
        self.click(self.SUCCESS_BUTTON)
    
    def click_danger_button(self):
        """点击危险按钮"""
        self.click(self.DANGER_BUTTON)
    
    def click_warning_button(self):
        """点击警告按钮"""
        self.click(self.WARNING_BUTTON)
    
    def open_modal(self):
        """打开弹窗"""
        self.click(self.MODAL_BUTTON)
    
    def close_modal(self):
        """关闭弹窗"""
        self.click(self.MODAL_CLOSE_BUTTON)
    
    def is_modal_visible(self):
        """判断弹窗是否可见"""
        modal = self.find_element(self.MODAL)
        return modal.is_displayed() and modal.value_of_css_property("display") != "none"
    
    def show_loading(self):
        """显示加载动画"""
        self.click(self.LOADING_BUTTON)
    
    def is_loader_visible(self):
        """判断加载动画是否可见"""
        return self.is_element_visible(self.LOADER)
