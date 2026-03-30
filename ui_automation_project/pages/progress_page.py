"""
Progress Page Object
进度条测试页面
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProgressPage(BasePage):
    """进度条测试页面"""
    
    PROGRESS_BAR = (By.ID, "progressBar")
    START_BUTTON = (By.XPATH, "//button[contains(text(), '开始进度')]")
    RESET_BUTTON = (By.XPATH, "//button[contains(text(), '重置') and contains(@onclick, 'resetProgress')]")
    
    def start_progress(self):
        """开始进度"""
        self.click(self.START_BUTTON)
    
    def reset_progress(self):
        """重置进度"""
        self.click(self.RESET_BUTTON)
    
    def get_progress_text(self):
        """获取进度文本"""
        return self.get_text(self.PROGRESS_BAR)
    
    def get_progress_width(self):
        """获取进度条宽度百分比"""
        bar = self.find_element(self.PROGRESS_BAR)
        return bar.text
