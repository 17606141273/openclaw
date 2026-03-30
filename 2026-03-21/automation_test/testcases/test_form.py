"""
test_form.py: 表单测试用例
"""
import pytest
import time
from selenium.webdriver.common.by import By


class TestForm:
    """表单功能测试"""

    def test_page_title(self, home_page):
        """验证页面标题"""
        title = home_page.get_text(home_page.TITLE)
        assert "自动化测试练习网站" in title

    def test_form_elements_visible(self, home_page):
        """验证表单元素都可见"""
        assert home_page.is_element_visible(home_page.USERNAME_INPUT)
        assert home_page.is_element_visible(home_page.EMAIL_INPUT)
        assert home_page.is_element_visible(home_page.PASSWORD_INPUT)
        assert home_page.is_element_visible(home_page.AGE_INPUT)
        assert home_page.is_element_visible(home_page.COUNTRY_SELECT)
        assert home_page.is_element_visible(home_page.DESCRIPTION_TEXTAREA)

    def test_fill_and_submit_form(self, home_page):
        """填写表单并提交"""
        home_page.fill_form(
            username="testuser",
            email="test@example.com",
            password="123456",
            age="25",
            birthday="1999-01-01",
            country="cn",
            gender="male",
            hobbies=["reading", "sports"],
            description="这是一段测试简介"
        )
        home_page.submit_form()

        # 验证成功提示
        assert home_page.is_element_visible(home_page.FORM_ALERT)
        alert_text = home_page.get_text(home_page.FORM_ALERT)
        assert "成功" in alert_text

    def test_form_validation_required_fields(self, home_page):
        """测试表单必填项验证"""
        # 不填必填项直接提交
        home_page.submit_form()
        # 页面应该阻止提交或显示验证提示
        # 取决于网站的实现，这里验证 input 的 required 属性生效
        username = home_page.find_element(home_page.USERNAME_INPUT)
        assert username.get_attribute("required") is not None

    def test_gender_selection(self, home_page):
        """测试性别单选框"""
        # 选择男性
        home_page.click(home_page.MALE_RADIO)
        assert home_page.find_element(home_page.MALE_RADIO).is_selected()

        # 选择女性
        home_page.click(home_page.FEMALE_RADIO)
        assert home_page.find_element(home_page.FEMALE_RADIO).is_selected()
        assert not home_page.find_element(home_page.MALE_RADIO).is_selected()

    def test_hobby_multi_select(self, home_page):
        """测试兴趣爱好多选"""
        home_page.click(home_page.HOBBY_READING)
        home_page.click(home_page.HOBBY_MUSIC)
        home_page.click(home_page.HOBBY_TRAVEL)

        assert home_page.find_element(home_page.HOBBY_READING).is_selected()
        assert home_page.find_element(home_page.HOBBY_MUSIC).is_selected()
        assert home_page.find_element(home_page.HOBBY_TRAVEL).is_selected()
        assert not home_page.find_element(home_page.HOBBY_SPORTS).is_selected()

    def test_country_dropdown(self, home_page):
        """测试国家下拉框"""
        home_page.click(home_page.COUNTRY_SELECT)

        # 获取所有选项
        options = home_page.find_elements(home_page.COUNTRY_OPTIONS)
        assert len(options) >= 5  # 至少5个国家选项

        # 选择日本
        home_page.select_country("jp")
        selected_option = home_page.find_element(
            (By.XPATH, "//select[@id='country']/option[@selected]")
        )
        assert selected_option.get_attribute("value") == "jp"

    def test_form_reset(self, home_page):
        """测试表单重置"""
        # 填写一些数据
        home_page.fill_form(
            username="before_reset",
            email="before@test.com",
            description="重置前的内容"
        )

        # 点击重置
        home_page.reset_form()

        # 验证表单已清空（重置后 input 的 value 应该为空或默认值）
        username_value = home_page.find_element(home_page.USERNAME_INPUT).get_attribute("value")
        email_value = home_page.find_element(home_page.EMAIL_INPUT).get_attribute("value")
        assert username_value == "" or username_value is None
        assert email_value == "" or email_value is None

    def test_birthday_input(self, home_page):
        """测试日期输入"""
        home_page.input_text(home_page.BIRTHDAY_INPUT, "2000-06-15")
        birthday_value = home_page.find_element(home_page.BIRTHDAY_INPUT).get_attribute("value")
        assert "2000-06-15" in birthday_value

    def test_age_input(self, home_page):
        """测试年龄输入"""
        home_page.input_text(home_page.AGE_INPUT, "30")
        age_value = home_page.find_element(home_page.AGE_INPUT).get_attribute("value")
        assert age_value == "30"
