"""
test_button.py: 按钮和弹窗测试用例
"""
import pytest
import time
from selenium.webdriver.common.by import By


class TestButton:
    """按钮功能测试"""

    def test_buttons_visible(self, home_page):
        """验证所有按钮可见"""
        assert home_page.is_element_visible(home_page.BTN_PRIMARY)
        assert home_page.is_element_visible(home_page.BTN_SUCCESS)
        assert home_page.is_element_visible(home_page.BTN_DANGER)
        assert home_page.is_element_visible(home_page.BTN_WARNING)

    def test_primary_button_click(self, home_page):
        """测试主要按钮点击"""
        home_page.click(home_page.BTN_PRIMARY)
        # 验证按钮可点击（无异常）
        assert home_page.is_element_clickable(home_page.BTN_PRIMARY)

    def test_success_button_click(self, home_page):
        """测试成功按钮点击"""
        home_page.click(home_page.BTN_SUCCESS)

    def test_danger_button_click(self, home_page):
        """测试危险按钮点击"""
        home_page.click(home_page.BTN_DANGER)

    def test_warning_button_click(self, home_page):
        """测试警告按钮点击"""
        home_page.click(home_page.BTN_WARNING)


class TestModal:
    """弹窗功能测试"""

    def test_open_modal(self, home_page):
        """测试打开弹窗"""
        home_page.open_modal()

        # 验证弹窗可见
        assert home_page.is_element_visible(home_page.MODAL)
        assert home_page.is_element_visible(home_page.MODAL_CONTENT)

    def test_modal_content(self, home_page):
        """测试弹窗内容"""
        home_page.open_modal()

        # 验证弹窗标题
        modal_title = home_page.get_text(home_page.MODAL_TITLE)
        assert "弹窗" in modal_title or "Modal" in modal_title

    def test_close_modal_by_button(self, home_page):
        """测试点击按钮关闭弹窗"""
        home_page.open_modal()
        assert home_page.is_element_visible(home_page.MODAL)

        # 点击关闭按钮
        home_page.close_modal()

        # 验证弹窗已关闭
        time.sleep(0.5)
        assert not home_page.is_element_visible(home_page.MODAL)

    def test_close_modal_by_outside(self, home_page):
        """测试点击弹窗外部关闭"""
        home_page.open_modal()
        assert home_page.is_element_visible(home_page.MODAL)

        # 点击外部区域
        home_page.click_modal_outside()

        # 验证弹窗已关闭
        time.sleep(0.5)
        assert not home_page.is_element_visible(home_page.MODAL)

    def test_modal_reopen(self, home_page):
        """测试弹窗关闭后可以重新打开"""
        home_page.open_modal()
        home_page.close_modal()
        time.sleep(0.3)

        home_page.open_modal()
        assert home_page.is_element_visible(home_page.MODAL)
