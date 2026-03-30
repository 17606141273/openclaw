"""
File Upload Page Object
文件上传测试页面
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class FileUploadPage(BasePage):
    """文件上传测试页面"""
    
    DROP_ZONE = (By.CSS_SELECTOR, ".drop-zone")
    FILE_INPUT = (By.ID, "fileInput")
    FILE_INFO = (By.ID, "fileInfo")
    
    def upload_file(self, file_path):
        """上传文件"""
        file_input = self.find_element(self.FILE_INPUT)
        file_input.send_keys(file_path)
    
    def get_file_info(self):
        """获取文件信息"""
        return self.get_text(self.FILE_INFO)
    
    def is_file_uploaded(self):
        """判断文件是否上传成功"""
        info = self.get_file_info()
        return "文件已选择" in info or "✅" in info
