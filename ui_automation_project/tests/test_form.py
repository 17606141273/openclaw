"""
Test Form
表单测试模块
"""

import pytest


class TestForm:
    """表单测试类"""
    
    def test_fill_username(self, form_page):
        """测试填写用户名"""
        form_page.fill_username("testuser")
        username_input = form_page.find_element(form_page.USERNAME_INPUT)
        assert username_input.get_attribute("value") == "testuser"
    
    def test_fill_email(self, form_page):
        """测试填写邮箱"""
        form_page.fill_email("test@example.com")
        email_input = form_page.find_element(form_page.EMAIL_INPUT)
        assert email_input.get_attribute("value") == "test@example.com"
    
    def test_fill_password(self, form_page):
        """测试填写密码"""
        form_page.fill_password("password123")
        password_input = form_page.find_element(form_page.PASSWORD_INPUT)
        assert password_input.get_attribute("value") == "password123"
    
    def test_fill_age(self, form_page):
        """测试填写年龄"""
        form_page.fill_age(25)
        age_input = form_page.find_element(form_page.AGE_INPUT)
        assert age_input.get_attribute("value") == "25"
    
    def test_fill_birthday(self, form_page):
        """测试填写生日"""
        form_page.fill_birthday("1999-01-01")
        birthday_input = form_page.find_element(form_page.BIRTHDAY_INPUT)
        assert birthday_input.get_attribute("value") == "1999-01-01"
    
    def test_select_country(self, form_page):
        """测试选择国家"""
        form_page.select_country("cn")
        country_select = form_page.find_element(form_page.COUNTRY_SELECT)
        assert country_select.get_attribute("value") == "cn"
    
    def test_select_gender(self, form_page):
        """测试选择性别"""
        form_page.select_gender("male")
        male_radio = form_page.find_element(form_page.MALE_RADIO)
        assert male_radio.is_selected()
    
    def test_select_hobbies(self, form_page):
        """测试选择兴趣爱好"""
        form_page.select_hobbies(["reading", "sports"])
        reading_checkbox = form_page.find_element(form_page.READING_CHECKBOX)
        sports_checkbox = form_page.find_element(form_page.SPORTS_CHECKBOX)
        assert reading_checkbox.is_selected()
        assert sports_checkbox.is_selected()
    
    def test_fill_description(self, form_page):
        """测试填写个人简介"""
        description = "这是一个测试简介"
        form_page.fill_description(description)
        desc_textarea = form_page.find_element(form_page.DESCRIPTION_TEXTAREA)
        assert desc_textarea.get_attribute("value") == description
    
    def test_submit_form_success(self, form_page):
        """测试成功提交表单"""
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        form_page.fill_complete_form(form_data)
        form_page.submit_form()
        
        alert = form_page.wait_for_alert()
        assert "表单提交成功" in alert.text
    
    def test_reset_form(self, form_page):
        """测试重置表单"""
        form_page.fill_username("testuser")
        form_page.reset_form()
        
        username_input = form_page.find_element(form_page.USERNAME_INPUT)
        assert username_input.get_attribute("value") == ""
    
    @pytest.mark.parametrize("country_code,expected", [
        ("cn", "中国"),
        ("us", "美国"),
        ("uk", "英国"),
        ("jp", "日本"),
        ("kr", "韩国"),
    ])
    def test_select_country_options(self, form_page, country_code, expected):
        """测试选择不同国家"""
        form_page.select_country(country_code)
        country_select = form_page.find_element(form_page.COUNTRY_SELECT)
        assert country_select.get_attribute("value") == country_code
    
    @pytest.mark.parametrize("gender", ["male", "female", "other"])
    def test_select_all_genders(self, form_page, gender):
        """测试选择所有性别选项"""
        form_page.select_gender(gender)
        gender_radio = form_page.find_element(getattr(form_page, f"{gender.upper()}_RADIO"))
        assert gender_radio.is_selected()
    
    def test_complete_form_submission(self, form_page):
        """测试完整表单提交"""
        form_data = {
            "username": "zhangsan",
            "email": "zhangsan@example.com",
            "password": "123456",
            "age": 25,
            "birthday": "1999-05-20",
            "country": "cn",
            "gender": "male",
            "hobbies": ["reading", "music"],
            "description": "我是一名软件测试工程师"
        }
        
        form_page.fill_complete_form(form_data)
        form_page.submit_form()
        
        alert = form_page.wait_for_alert()
        assert "表单提交成功" in alert.text
