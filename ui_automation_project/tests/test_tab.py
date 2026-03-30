"""
Test Tab
标签页测试模块
"""


class TestTab:
    """标签页测试类"""
    
    def test_switch_to_home_tab(self, tab_page):
        """测试切换到首页标签"""
        tab_page.switch_to_home()
        assert tab_page.is_tab_active("home")
        assert tab_page.is_content_visible("home")
    
    def test_switch_to_product_tab(self, tab_page):
        """测试切换到产品标签"""
        tab_page.switch_to_product()
        assert tab_page.is_tab_active("product")
        assert tab_page.is_content_visible("product")
    
    def test_switch_to_about_tab(self, tab_page):
        """测试切换到关于标签"""
        tab_page.switch_to_about()
        assert tab_page.is_tab_active("about")
        assert tab_page.is_content_visible("about")
    
    def test_tab_content_text(self, tab_page):
        """测试标签页内容文本"""
        tab_page.switch_to_home()
        content = tab_page.get_tab_content_text("home")
        assert "欢迎来到首页" in content
        
        tab_page.switch_to_product()
        content = tab_page.get_tab_content_text("product")
        assert "产品列表" in content
        
        tab_page.switch_to_about()
        content = tab_page.get_tab_content_text("about")
        assert "关于我们" in content
    
    def test_tab_switch_sequence(self, tab_page):
        """测试标签页切换序列"""
        tab_page.switch_to_home()
        assert tab_page.is_content_visible("home")
        
        tab_page.switch_to_product()
        assert tab_page.is_content_visible("product")
        
        tab_page.switch_to_about()
        assert tab_page.is_content_visible("about")
        
        tab_page.switch_to_home()
        assert tab_page.is_content_visible("home")
    
    def test_all_tabs_clickable(self, tab_page):
        """测试所有标签可点击"""
        tabs = [tab_page.TAB_HOME, tab_page.TAB_PRODUCT, tab_page.TAB_ABOUT]
        for tab in tabs:
            assert tab_page.is_element_visible(tab)
