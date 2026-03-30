"""
Test Integration
集成测试模块
"""

import time


class TestIntegration:
    """集成测试类"""
    
    def test_complete_workflow(self, driver, form_page, button_page, tab_page, table_page):
        """测试完整工作流程"""
        # 1. 填写并提交表单
        form_data = {
            "username": "integration_test",
            "email": "test@test.com",
            "password": "test123",
            "country": "cn",
            "gender": "male"
        }
        form_page.fill_complete_form(form_data)
        form_page.submit_form()
        
        alert = form_page.wait_for_alert()
        assert "表单提交成功" in alert.text
        
        # 2. 点击按钮
        button_page.click_success_button()
        alert = button_page.wait_for_alert()
        assert "成功按钮" in alert.text
        
        # 3. 切换标签页
        tab_page.switch_to_product()
        assert tab_page.is_content_visible("product")
        
        # 4. 验证表格数据
        row_data = table_page.get_row_data(0)
        assert row_data[1] == "张三"
    
    def test_error_handling(self, form_page):
        """测试错误处理"""
        form_page.submit_form()
        assert form_page.is_element_visible(form_page.USERNAME_INPUT)
    
    def test_multiple_operations_sequence(self, form_page, button_page, tab_page):
        """测试多操作序列"""
        # 操作序列：提交表单 -> 点击按钮 -> 切换标签
        form_data = {"username": "seq_test", "email": "seq@test.com", "password": "123"}
        form_page.fill_complete_form(form_data)
        form_page.submit_form()
        
        time.sleep(0.5)
        button_page.click_primary_button()
        
        time.sleep(0.5)
        tab_page.switch_to_about()
        assert tab_page.is_content_visible("about")
