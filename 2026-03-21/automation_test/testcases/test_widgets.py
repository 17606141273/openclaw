"""
test_widgets.py: 进度条、标签页、表格、文件上传测试用例
"""
import pytest
import time


class TestProgressBar:
    """进度条功能测试"""

    def test_progress_bar_visible(self, home_page):
        """验证进度条可见"""
        assert home_page.is_element_visible(home_page.PROGRESS_BAR)

    def test_start_progress(self, home_page):
        """测试开始进度条"""
        home_page.start_progress()

        # 等待进度条动画
        time.sleep(2)

        # 验证进度条有变化（不等于0）
        progress_style = home_page.get_attribute(home_page.PROGRESS_BAR, "style")
        assert "width" in progress_style

    def test_progress_completes(self, home_page):
        """测试进度条完成到100%"""
        home_page.start_progress()

        # 等待进度条完成（最多15秒）
        max_wait = 15
        start_time = time.time()
        while time.time() - start_time < max_wait:
            progress_style = home_page.get_attribute(home_page.PROGRESS_BAR, "style")
            if "100%" in progress_style:
                break
            time.sleep(0.5)

        # 验证进度条到100%
        progress_style = home_page.get_attribute(home_page.PROGRESS_BAR, "style")
        assert "100%" in progress_style

    def test_reset_progress(self, home_page):
        """测试重置进度条"""
        # 先启动进度条
        home_page.start_progress()
        time.sleep(1)

        # 点击重置
        home_page.reset_progress()
        time.sleep(0.5)

        # 验证进度条回到0
        progress_style = home_page.get_attribute(home_page.PROGRESS_BAR, "style")
        assert "0%" in progress_style or "width: 0" in progress_style


class TestTabs:
    """标签页功能测试"""

    def test_tabs_visible(self, home_page):
        """验证标签页可见"""
        assert home_page.is_element_visible(home_page.TAB_1)
        assert home_page.is_element_visible(home_page.TAB_2)
        assert home_page.is_element_visible(home_page.TAB_3)

    def test_default_active_tab(self, home_page):
        """测试默认激活的标签页"""
        # 首页应该是默认显示的
        assert home_page.is_element_visible(home_page.TAB_CONTENT_1)

    def test_switch_to_tab2(self, home_page):
        """测试切换到第二个标签页"""
        home_page.switch_tab(2)

        # 验证第二个标签页内容可见
        assert home_page.is_element_visible(home_page.TAB_CONTENT_2)

    def test_switch_to_tab3(self, home_page):
        """测试切换到第三个标签页"""
        home_page.switch_tab(3)
        assert home_page.is_element_visible(home_page.TAB_CONTENT_3)

    def test_tab_switching(self, home_page):
        """测试标签页切换"""
        # 切换到产品
        home_page.switch_tab(2)
        assert home_page.is_element_visible(home_page.TAB_CONTENT_2)

        # 切换到关于
        home_page.switch_tab(3)
        assert home_page.is_element_visible(home_page.TAB_CONTENT_3)

        # 切换回首页
        home_page.switch_tab(1)
        assert home_page.is_element_visible(home_page.TAB_CONTENT_1)


class TestTable:
    """表格功能测试"""

    def test_table_visible(self, home_page):
        """验证表格可见"""
        assert home_page.is_element_visible(home_page.DATA_TABLE)

    def test_table_headers(self, home_page):
        """验证表格表头"""
        headers = home_page.find_elements(home_page.TABLE_HEADERS)
        header_texts = [h.text for h in headers]
        assert "姓名" in header_texts or "Name" in header_texts

    def test_table_row_count(self, home_page):
        """测试表格行数"""
        row_count = home_page.get_table_row_count()
        assert row_count >= 3  # 至少3行数据

    def test_get_table_data(self, home_page):
        """测试获取表格数据"""
        data = home_page.get_table_data()
        assert len(data) >= 3
        assert len(data[0]) >= 4  # 每行至少4列

    def test_edit_button_click(self, home_page):
        """测试编辑按钮可点击"""
        edit_btns = home_page.find_elements(home_page.EDIT_BTNS)
        assert len(edit_btns) >= 3
        assert home_page.is_element_clickable(home_page.EDIT_BTNS)


class TestFileUpload:
    """文件上传功能测试"""

    def test_drop_zone_visible(self, home_page):
        """验证上传区域可见"""
        assert home_page.is_element_visible(home_page.DROP_ZONE)

    def test_file_input_exists(self, home_page):
        """验证文件输入框存在"""
        assert home_page.is_element_visible(home_page.FILE_INPUT)

    def test_upload_small_file(self, home_page, tmp_path):
        """测试上传小文件"""
        # 创建一个临时测试文件
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content for automation")

        # 执行上传
        home_page.upload_file(str(test_file))

        # 验证文件信息显示（如果有的话）
        # 根据实际页面实现验证


class TestLoading:
    """加载动画测试"""

    def test_show_loading_button(self, home_page):
        """测试显示加载按钮"""
        assert home_page.is_element_visible(home_page.BTN_SHOW_LOADING)

    def test_loading_display(self, home_page):
        """测试加载动画显示"""
        home_page.click(home_page.BTN_SHOW_LOADING)
        time.sleep(0.5)

        # 验证加载动画可见
        assert home_page.is_element_visible(home_page.LOADER)
