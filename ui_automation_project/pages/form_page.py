"""
Form Page Object
表单测试页面
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage


class FormPage(BasePage):
    """表单测试页面"""
    
    # 定位器
    USERNAME_INPUT = (By.ID, "username")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    AGE_INPUT = (By.ID, "age")
    BIRTHDAY_INPUT = (By.ID, "birthday")
    COUNTRY_SELECT = (By.ID, "country")
    DESCRIPTION_TEXTAREA = (By.ID, "description")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.CSS_SELECTOR, "button[type='reset']")
    ALERT_DIV = (By.ID, "formAlert")
    
    # 性别单选框
    MALE_RADIO = (By.ID, "male")
    FEMALE_RADIO = (By.ID, "female")
    OTHER_RADIO = (By.ID, "other")
    
    # 兴趣爱好复选框
    READING_CHECKBOX = (By.ID, "reading")
    SPORTS_CHECKBOX = (By.ID, "sports")
    MUSIC_CHECKBOX = (By.ID, "music")
    TRAVEL_CHECKBOX = (By.ID, "travel")
    
    def fill_username(self, username):
        """填写用户名"""
        self.send_keys(self.USERNAME_INPUT, username)
    
    def fill_email(self, email):
        """填写邮箱"""
        self.send_keys(self.EMAIL_INPUT, email)
    
    def fill_password(self, password):
        """填写密码"""
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def fill_age(self, age):
        """填写年龄"""
        self.send_keys(self.AGE_INPUT, str(age))
    
    def fill_birthday(self, birthday):
        """填写生日"""
        self.send_keys(self.BIRTHDAY_INPUT, birthday)
    
    def select_country(self, country_value):
        """选择国家"""
        select = Select(self.find_element(self.COUNTRY_SELECT))
        select.select_by_value(country_value)
    
    def select_gender(self, gender):
        """选择性别"""
        if gender == "male":
            self.click(self.MALE_RADIO)
        elif gender == "female":
            self.click(self.FEMALE_RADIO)
        elif gender == "other":
            self.click(self.OTHER_RADIO)
    
    def select_hobbies(self, hobbies):
        """选择兴趣爱好"""
        hobby_map = {
            "reading": self.READING_CHECKBOX,
            "sports": self.SPORTS_CHECKBOX,
            "music": self.MUSIC_CHECKBOX,
            "travel": self.TRAVEL_CHECKBOX
        }
        for hobby in hobbies:
            if hobby in hobby_map:
                self.click(hobby_map[hobby])
    
    def fill_description(self, description):
        """填写个人简介"""
        self.send_keys(self.DESCRIPTION_TEXTAREA, description)
    
    def submit_form(self):
        """提交表单"""
        self.click(self.SUBMIT_BUTTON)
    
    def reset_form(self):
        """重置表单"""
        self.click(self.RESET_BUTTON)
    
    def get_alert_text(self):
        """获取提示消息文本"""
        return self.get_text(self.ALERT_DIV)
    
    def is_alert_visible(self):
        """判断提示消息是否可见"""
        return self.is_element_visible(self.ALERT_DIV)
    
    def fill_complete_form(self, data):
        """填写完整表单"""
        self.fill_username(data.get("username", ""))
        self.fill_email(data.get("email", ""))
        self.fill_password(data.get("password", ""))
        if "age" in data:
            self.fill_age(data["age"])
        if "birthday" in data:
            self.fill_birthday(data["birthday"])
        if "country" in data:
            self.select_country(data["country"])
        if "gender" in data:
            self.select_gender(data["gender"])
        if "hobbies" in data:
            self.select_hobbies(data["hobbies"])
        if "description" in data:
            self.fill_description(data["description"])
