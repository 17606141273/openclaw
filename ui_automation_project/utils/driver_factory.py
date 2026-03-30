"""
Driver Utility
浏览器驱动工具类
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os


class DriverFactory:
    """驱动工厂类"""
    
    @staticmethod
    def create_driver(headless=True, window_size="1920,1080", browser="edge"):
        """
        创建浏览器驱动
        
        Args:
            headless: 是否无头模式
            window_size: 窗口大小
            browser: 浏览器类型 (chrome/edge)
        
        Returns:
            WebDriver 实例
        """
        if browser.lower() == "chrome":
            return DriverFactory._create_chrome_driver(headless, window_size)
        else:
            return DriverFactory._create_edge_driver(headless, window_size)
    
    @staticmethod
    def _create_chrome_driver(headless, window_size):
        """创建 Chrome 驱动"""
        chrome_options = ChromeOptions()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--window-size={window_size}")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        
        # 使用本地已有的驱动或自动下载
        try:
            service = ChromeService(ChromeDriverManager().install())
        except:
            # 如果下载失败，使用本地驱动
            local_driver = r"C:\Users\29210\.wdm\drivers\chromedriver\win64\114.0.5735.90\chromedriver.exe"
            service = ChromeService(local_driver)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver
    
    @staticmethod
    def _create_edge_driver(headless, window_size):
        """创建 Edge 驱动"""
        edge_options = EdgeOptions()
        
        if headless:
            edge_options.add_argument("--headless")
        
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument(f"--window-size={window_size}")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--disable-extensions")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        
        return driver
    
    @staticmethod
    def get_test_page_url():
        """获取测试页面 URL"""
        test_file_path = os.path.abspath("D:/AI_Files/automation-test-practice.html")
        return f"file:///{test_file_path}"
