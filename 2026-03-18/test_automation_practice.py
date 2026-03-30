"""
UI自动化测试项目 - Page Object Model 模式
测试目标: automation-test-practice.html
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import os
import time


# ==================== Base Page ====================
class BasePage:
    """基础页面类，封装通用方法"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
    
    def open(self, url):
        """打开网页"""
        self.driver.get(url)
    
    def find_element(self, locator):
        """查找元素"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """查找多个元素"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click(self, locator):
        """点击元素"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys(self, locator, text):
        """输入文本"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """获取元素文本"""
        return self.find_element(locator).text
    
    def is_element_visible(self, locator):
        """判断元素是否可见"""
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False
    
    def wait_for_alert(self):
        """等待提示消息出现"""
        return self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
        )
    
    def scroll_to_element(self, locator):
        """滚动到元素"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)


# ==================== Form Page ====================
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
        from selenium.webdriver.support.ui import Select
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


# ==================== Button Page ====================
class ButtonPage(BasePage):
    """按钮测试页面"""
    
    PRIMARY_BUTTON = (By.XPATH, "//button[contains(text(), '主要按钮')]")
    SUCCESS_BUTTON = (By.XPATH, "//button[contains(text(), '成功按钮')]")
    DANGER_BUTTON = (By.XPATH, "//button[contains(text(), '危险按钮')]")
    WARNING_BUTTON = (By.XPATH, "//button[contains(text(), '警告按钮')]")
    MODAL_BUTTON = (By.XPATH, "//button[contains(text(), '打开弹窗')]")
    LOADING_BUTTON = (By.XPATH, "//button[contains(text(), '显示加载')]")
    
    MODAL = (By.ID, "modal")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//div[@id='modal']//button[contains(text(), '关闭')]")
    LOADER = (By.ID, "loader")
    
    def click_primary_button(self):
        """点击主要按钮"""
        self.click(self.PRIMARY_BUTTON)
    
    def click_success_button(self):
        """点击成功按钮"""
        self.click(self.SUCCESS_BUTTON)
    
    def click_danger_button(self):
        """点击危险按钮"""
        self.click(self.DANGER_BUTTON)
    
    def click_warning_button(self):
        """点击警告按钮"""
        self.click(self.WARNING_BUTTON)
    
    def open_modal(self):
        """打开弹窗"""
        self.click(self.MODAL_BUTTON)
    
    def close_modal(self):
        """关闭弹窗"""
        self.click(self.MODAL_CLOSE_BUTTON)
    
    def is_modal_visible(self):
        """判断弹窗是否可见"""
        modal = self.find_element(self.MODAL)
        return modal.is_displayed() and modal.value_of_css_property("display") != "none"
    
    def show_loading(self):
        """显示加载动画"""
        self.click(self.LOADING_BUTTON)
    
    def is_loader_visible(self):
        """判断加载动画是否可见"""
        return self.is_element_visible(self.LOADER)


# ==================== Progress Page ====================
class ProgressPage(BasePage):
    """进度条测试页面"""
    
    PROGRESS_BAR = (By.ID, "progressBar")
    START_BUTTON = (By.XPATH, "//button[contains(text(), '开始进度')]")
    RESET_BUTTON = (By.XPATH, "//button[contains(text(), '重置') and contains(@onclick, 'resetProgress')]")
    
    def start_progress(self):
        """开始进度"""
        self.click(self.START_BUTTON)
    
    def reset_progress(self):
        """重置进度"""
        self.click(self.RESET_BUTTON)
    
    def get_progress_text(self):
        """获取进度文本"""
        return self.get_text(self.PROGRESS_BAR)
    
    def get_progress_width(self):
        """获取进度条宽度百分比"""
        bar = self.find_element(self.PROGRESS_BAR)
        width = bar.value_of_css_property("width")
        # 返回百分比数值
        return bar.text


# ==================== Tab Page ====================
class TabPage(BasePage):
    """标签页测试页面"""
    
    TAB_HOME = (By.XPATH, "//button[@class='tab' and contains(text(), '首页')]")
    TAB_PRODUCT = (By.XPATH, "//button[@class='tab' and contains(text(), '产品')]")
    TAB_ABOUT = (By.XPATH, "//button[@class='tab' and contains(text(), '关于')]")
    
    TAB_CONTENT_HOME = (By.ID, "tab1")
    TAB_CONTENT_PRODUCT = (By.ID, "tab2")
    TAB_CONTENT_ABOUT = (By.ID, "tab3")
    
    def switch_to_home(self):
        """切换到首页"""
        self.click(self.TAB_HOME)
    
    def switch_to_product(self):
        """切换到产品页"""
        self.click(self.TAB_PRODUCT)
    
    def switch_to_about(self):
        """切换到关于页"""
        self.click(self.TAB_ABOUT)
    
    def is_tab_active(self, tab_name):
        """判断标签页是否激活"""
        tab_map = {
            "home": self.TAB_HOME,
            "product": self.TAB_PRODUCT,
            "about": self.TAB_ABOUT
        }
        tab = self.find_element(tab_map.get(tab_name))
        return "active" in tab.get_attribute("class")
    
    def is_content_visible(self, content_name):
        """判断内容是否可见"""
        content_map = {
            "home": self.TAB_CONTENT_HOME,
            "product": self.TAB_CONTENT_PRODUCT,
            "about": self.TAB_CONTENT_ABOUT
        }
        content = self.find_element(content_map.get(content_name))
        return content.is_displayed() and "active" in content.get_attribute("class")
    
    def get_tab_content_text(self, content_name):
        """获取标签页内容文本"""
        content_map = {
            "home": self.TAB_CONTENT_HOME,
            "product": self.TAB_CONTENT_PRODUCT,
            "about": self.TAB_CONTENT_ABOUT
        }
        return self.get_text(content_map.get(content_name))


# ==================== Table Page ====================
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


# ==================== File Upload Page ====================
class FileUploadPage(BasePage):
    """文件上传测试页面"""
    
    DROP_ZONE = (By.CSS_SELECTOR, ".drop-zone")
    FILE_INPUT = (By.ID, "fileInput")
    FILE_INFO = (By.ID, "fileInfo")
    
    def upload_file(self, file_path):
        """上传文件"""
        file_input = self.find_element(self.FILE_INPUT)
        file_input.send_keys(file_path)
    
    def get_file_info(self):
        """获取文件信息"""
        return self.get_text(self.FILE_INFO)
    
    def is_file_uploaded(self):
        """判断文件是否上传成功"""
        info = self.get_file_info()
        return "文件已选择" in info or "✅" in info


# ==================== Pytest Fixtures ====================
@pytest.fixture(scope="function")
def driver():
    """创建浏览器驱动"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # 打开测试页面
    test_file_path = os.path.abspath("D:/AI_Files/automation-test-practice.html")
    driver.get(f"file:///{test_file_path}")
    
    yield driver
    
    driver.quit()


@pytest.fixture
def form_page(driver):
    """表单页面对象"""
    return FormPage(driver)


@pytest.fixture
def button_page(driver):
    """按钮页面对象"""
    return ButtonPage(driver)


@pytest.fixture
def progress_page(driver):
    """进度条页面对象"""
    return ProgressPage(driver)


@pytest.fixture
def tab_page(driver):
    """标签页页面对象"""
    return TabPage(driver)


@pytest.fixture
def table_page(driver):
    """表格页面对象"""
    return TablePage(driver)


@pytest.fixture
def file_upload_page(driver):
    """文件上传页面对象"""
    return FileUploadPage(driver)


# ==================== Test Cases - Form ====================
class TestForm:
    """表单测试类"""
    
    def test_fill_username(self, form_page):
        """测试填写用户名"""
        form_page.fill_username("testuser")
        # 验证输入成功
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
        
        # 等待提示消息
        alert = form_page.wait_for_alert()
        assert "表单提交成功" in alert.text
    
    def test_reset_form(self, form_page):
        """测试重置表单"""
        form_page.fill_username("testuser")
        form_page.reset_form()
        
        username_input = form_page.find_element(form_page.USERNAME_INPUT)
        assert username_input.get_attribute("value") == ""
    
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


# ==================== Test Cases - Button ====================
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
        time.sleep(0.5)  # 等待动画
        assert not button_page.is_modal_visible()
    
    def test_show_loading(self, button_page):
        """测试显示加载动画"""
        button_page.show_loading()
        assert button_page.is_loader_visible()
        
        # 等待加载完成
        time.sleep(3.5)
        assert not button_page.is_loader_visible()


# ==================== Test Cases - Progress ====================
class TestProgress:
    """进度条测试类"""
    
    def test_start_progress(self, progress_page):
        """测试开始进度"""
        progress_page.start_progress()
        time.sleep(1)
        
        progress_text = progress_page.get_progress_text()
        assert "%" in progress_text
    
    def test_progress_completion(self, progress_page):
        """测试进度完成"""
        progress_page.start_progress()
        
        # 等待进度完成（约5秒）
        time.sleep(6)
        
        progress_text = progress_page.get_progress_text()
        assert progress_text == "100%"
    
    def test_reset_progress(self, progress_page):
        """测试重置进度"""
        progress_page.start_progress()
        time.sleep(1)
        progress_page.reset_progress()
        
        progress_text = progress_page.get_progress_text()
        assert progress_text == "0%"


# ==================== Test Cases - Tab ====================
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
        # 首页 -> 产品 -> 关于 -> 首页
        tab_page.switch_to_home()
        assert tab_page.is_content_visible("home")
        
        tab_page.switch_to_product()
        assert tab_page.is_content_visible("product")
        
        tab_page.switch_to_about()
        assert tab_page.is_content_visible("about")
        
        tab_page.switch_to_home()
        assert tab_page.is_content_visible("home")


# ==================== Test Cases - Table ====================
class TestTable:
    """表格测试类"""
    
    def test_table_rows_count(self, table_page):
        """测试表格行数"""
        count = table_page.get_table_rows_count()
        assert count == 4  # 根据HTML，应该有4行数据
    
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
        
        # 验证第一行数据
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
        
        # 验证提示消息
        from selenium.webdriver.common.by import By
        alert = WebDriverWait(table_page.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
        )
        assert "正在编辑: 张三" in alert.text


# ==================== Test Cases - File Upload ====================
class TestFileUpload:
    """文件上传测试类"""
    
    def test_upload_text_file(self, file_upload_page, tmp_path):
        """测试上传文本文件"""
        # 创建临时文件
        test_file = tmp_path / "test.txt"
        test_file.write_text("这是一个测试文件")
        
        file_upload_page.upload_file(str(test_file))
        time.sleep(1)
        
        assert file_upload_page.is_file_uploaded()
        file_info = file_upload_page.get_file_info()
        assert "test.txt" in file_info
    
    def test_upload_file_info_display(self, file_upload_page, tmp_path):
        """测试上传文件信息显示"""
        test_file = tmp_path / "test_document.pdf"
        test_file.write_bytes(b"PDF content" * 100)
        
        file_upload_page.upload_file(str(test_file))
        time.sleep(1)
        
        file_info = file_upload_page.get_file_info()
        assert "test_document.pdf" in file_info
        assert "KB" in file_info


# ==================== Integration Tests ====================
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
        # 不填写必填项直接提交
        form_page.submit_form()
        
        # 浏览器会阻止提交，验证页面未跳转
        assert form_page.is_element_visible(form_page.USERNAME_INPUT)


# ==================== Main ====================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
