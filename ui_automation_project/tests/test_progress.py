"""
Test Progress
进度条测试模块
"""

import time


class TestProgress:
    """进度条测试类"""
    
    def test_start_progress(self, progress_page):
        """测试开始进度"""
        progress_page.start_progress()
        time.sleep(1)
        
        progress_text = progress_page.get_progress_text()
        assert "%" in progress_text
    
    def test_progress_completion(self, progress_page):
        """测试进度完成"""
        progress_page.start_progress()
        time.sleep(6)
        
        progress_text = progress_page.get_progress_text()
        assert progress_text == "100%"
    
    def test_reset_progress(self, progress_page):
        """测试重置进度"""
        progress_page.start_progress()
        time.sleep(1)
        progress_page.reset_progress()
        
        progress_text = progress_page.get_progress_text()
        assert progress_text == "0%"
    
    def test_progress_increases(self, progress_page):
        """测试进度增加"""
        progress_page.start_progress()
        time.sleep(1)
        progress1 = int(progress_page.get_progress_text().replace("%", ""))
        
        time.sleep(2)
        progress2 = int(progress_page.get_progress_text().replace("%", ""))
        
        assert progress2 > progress1
