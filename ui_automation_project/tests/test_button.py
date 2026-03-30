"""
Test Button
按钮测试模块
"""

import time


class TestButton:
    """按钮测试类"""
    
    def test_click_primary_button(self, button_page):
        """测试点击主要按钮"""
        button_page.click_primary_button()
        alert = button_page.wait_for_alert()
        assert "主要按钮" in alert.text
    
    def test_click_success_button(self, button_page):
        """测试点击成功按钮"""
        button_page.click_success_button()
        alert = button_page.wait_for_alert()
        assert "成功按钮" in alert.text
    
    def test_click_danger_button(self, button_page):
        """测试点击危险按钮"""
        button_page.click_danger_button()
        alert = button_page.wait_for_alert()
        assert "危险按钮" in alert.text
    
    def test_click_warning_button(self, button_page):
        """测试点击警告按钮"""
        button_page.click_warning_button()
        alert = button_page.wait_for_alert()
        assert "警告按钮" in alert.text
    
    def test_open_and_close_modal(self, button_page):
        """测试打开和关闭弹窗"""
        button_page.open_modal()
        assert button_page.is_modal_visible()
        
        button_page.close_modal()
        time.sleep(0.5)
        assert not button_page.is_modal_visible()
    
    def test_show_loading(self, button_page):
        """测试显示加载动画"""
        button_page.show_loading()
        assert button_page.is_loader_visible()
        
        time.sleep(3.5)
        assert not button_page.is_loader_visible()
    
    def test_all_buttons_clickable(self, button_page):
        """测试所有按钮可点击"""
        buttons = [
            button_page.PRIMARY_BUTTON,
            button_page.SUCCESS_BUTTON,
            button_page.DANGER_BUTTON,
            button_page.WARNING_BUTTON,
            button_page.MODAL_BUTTON,
            button_page.LOADING_BUTTON
        ]
        
        for button in buttons:
            assert button_page.is_element_visible(button)
