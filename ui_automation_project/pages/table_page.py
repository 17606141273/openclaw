"""
Table Page Object
表格测试页面
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class TablePage(BasePage):
    """表格测试页面"""
    
    TABLE = (By.ID, "dataTable")
    TABLE_ROWS = (By.CSS_SELECTOR, "#dataTable tbody tr")
    
    def get_table_rows_count(self):
        """获取表格行数"""
        return len(self.find_elements(self.TABLE_ROWS))
    
    def get_row_data(self, row_index):
        """获取指定行数据"""
        rows = self.find_elements(self.TABLE_ROWS)
        if row_index < len(rows):
            cells = rows[row_index].find_elements(By.TAG_NAME, "td")
            return [cell.text for cell in cells]
        return None
    
    def get_all_table_data(self):
        """获取所有表格数据"""
        rows = self.find_elements(self.TABLE_ROWS)
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            data.append([cell.text for cell in cells])
        return data
    
    def click_edit_button(self, row_index):
        """点击指定行的编辑按钮"""
        rows = self.find_elements(self.TABLE_ROWS)
        if row_index < len(rows):
            edit_btn = rows[row_index].find_element(By.XPATH, ".//button[contains(text(), '编辑')]")
            edit_btn.click()
    
    def find_row_by_name(self, name):
        """根据姓名查找行"""
        rows = self.find_elements(self.TABLE_ROWS)
        for i, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 1 and cells[1].text == name:
                return i
        return -1
