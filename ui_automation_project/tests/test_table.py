"""
Test Table
表格测试模块
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestTable:
    """表格测试类"""
    
    def test_table_rows_count(self, table_page):
        """测试表格行数"""
        count = table_page.get_table_rows_count()
        assert count == 4
    
    def test_get_row_data(self, table_page):
        """测试获取行数据"""
        row_data = table_page.get_row_data(0)
        assert row_data[0] == "001"
        assert row_data[1] == "张三"
        assert row_data[2] == "测试工程师"
    
    def test_get_all_table_data(self, table_page):
        """测试获取所有表格数据"""
        all_data = table_page.get_all_table_data()
        assert len(all_data) == 4
        
        assert all_data[0][1] == "张三"
        assert all_data[1][1] == "李四"
        assert all_data[2][1] == "王五"
        assert all_data[3][1] == "赵六"
    
    def test_find_row_by_name(self, table_page):
        """测试根据姓名查找行"""
        row_index = table_page.find_row_by_name("李四")
        assert row_index == 1
        
        row_index = table_page.find_row_by_name("不存在")
        assert row_index == -1
    
    def test_click_edit_button(self, table_page):
        """测试点击编辑按钮"""
        table_page.click_edit_button(0)
        
        alert = WebDriverWait(table_page.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
        )
        assert "正在编辑: 张三" in alert.text
    
    def test_table_headers(self, table_page):
        """测试表格表头"""
        headers = table_page.driver.find_elements(By.CSS_SELECTOR, "#dataTable th")
        header_texts = [h.text for h in headers]
        
        assert "ID" in header_texts
        assert "姓名" in header_texts
        assert "职位" in header_texts
        assert "部门" in header_texts
        assert "操作" in header_texts
