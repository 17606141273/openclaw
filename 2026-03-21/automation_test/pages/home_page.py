"""
HomePage: 首页（主容器）页面对象
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """首页页面对象"""

    # ========== 页面元素 ==========
    # 标题
    TITLE = (By.CSS_SELECTOR, "h1")
    SUBTITLE = (By.CSS_SELECTOR, ".subtitle")

    # ========== 表单测试区域 ==========
    FORM_SECTION = (By.CSS_SELECTOR, ".section:nth-child(2)")
    USERNAME_INPUT = (By.ID, "username")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    AGE_INPUT = (By.ID, "age")
    BIRTHDAY_INPUT = (By.ID, "birthday")
    COUNTRY_SELECT = (By.ID, "country")
    COUNTRY_OPTIONS = (By.CSS_SELECTOR, "#country option")
    MALE_RADIO = (By.ID, "male")
    FEMALE_RADIO = (By.ID, "female")
    OTHER_RADIO = (By.ID, "other")
    HOBBY_READING = (By.ID, "reading")
    HOBBY_SPORTS = (By.ID, "sports")
    HOBBY_MUSIC = (By.ID, "music")
    HOBBY_TRAVEL = (By.ID, "travel")
    DESCRIPTION_TEXTAREA = (By.ID, "description")
    FORM_SUBMIT_BTN = (By.CSS_SELECTOR, "#testForm button[type='submit']")
    FORM_RESET_BTN = (By.CSS_SELECTOR, "#testForm button[type='reset']")
    FORM_ALERT = (By.ID, "formAlert")

    # ========== 按钮测试区域 ==========
    BTN_PRIMARY = (By.XPATH, "//button[contains(@class,'btn-primary') and contains(text(),'主要')]")
    BTN_SUCCESS = (By.XPATH, "//button[contains(@class,'btn-success') and contains(text(),'成功')]")
    BTN_DANGER = (By.XPATH, "//button[contains(@class,'btn-danger') and contains(text(),'危险')]")
    BTN_WARNING = (By.XPATH, "//button[contains(@class,'btn-warning') and contains(text(),'警告')]")
    BTN_OPEN_MODAL = (By.XPATH, "//button[contains(text(),'打开弹窗')]")
    BTN_SHOW_LOADING = (By.XPATH, "//button[contains(text(),'显示加载')]")

    # ========== 进度条区域 ==========
    PROGRESS_SECTION = (By.CSS_SELECTOR, ".section:nth-child(4)")
    PROGRESS_BAR = (By.ID, "progressBar")
    BTN_START_PROGRESS = (By.XPATH, "//button[contains(text(),'开始进度')]")
    BTN_RESET_PROGRESS = (By.XPATH, "//button[contains(text(),'重置')]")

    # ========== 标签页区域 ==========
    TABS_SECTION = (By.CSS_SELECTOR, ".section:nth-child(5)")
    TAB_1 = (By.XPATH, "//button[@class='tab' and contains(text(),'首页')]")
    TAB_2 = (By.XPATH, "//button[@class='tab' and contains(text(),'产品')]")
    TAB_3 = (By.XPATH, "//button[@class='tab' and contains(text(),'关于')]")
    TAB_CONTENT_1 = (By.ID, "tab1")
    TAB_CONTENT_2 = (By.ID, "tab2")
    TAB_CONTENT_3 = (By.ID, "tab3")

    # ========== 表格区域 ==========
    TABLE_SECTION = (By.CSS_SELECTOR, ".section:nth-child(6)")
    DATA_TABLE = (By.ID, "dataTable")
    TABLE_ROWS = (By.CSS_SELECTOR, "#dataTable tbody tr")
    TABLE_HEADERS = (By.CSS_SELECTOR, "#dataTable thead th")
    EDIT_BTNS = (By.XPATH, "//button[contains(text(),'编辑')]")

    # ========== 文件上传区域 ==========
    UPLOAD_SECTION = (By.CSS_SELECTOR, ".section:nth-child(7)")
    DROP_ZONE = (By.CSS_SELECTOR, ".drop-zone")
    FILE_INPUT = (By.ID, "fileInput")
    FILE_INFO = (By.ID, "fileInfo")

    # ========== 加载动画 ==========
    LOADER = (By.ID, "loader")

    # ========== 弹窗 ==========
    MODAL = (By.ID, "modal")
    MODAL_CONTENT = (By.CSS_SELECTOR, ".modal-content")
    MODAL_CLOSE_BTN = (By.XPATH, "//button[contains(text(),'关闭')]")
    MODAL_TITLE = (By.CSS_SELECTOR, ".modal-content h2")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("file:///D:/AI_Files/2026-03-21/automation-test-practice.html")

    # ========== 页面操作方法 ==========

    def fill_form(self, username="", email="", password="", age="", birthday="",
                  country="", gender="", hobbies=None, description=""):
        """填写表单"""
        if username:
            self.input_text(self.USERNAME_INPUT, username)
        if email:
            self.input_text(self.EMAIL_INPUT, email)
        if password:
            self.input_text(self.PASSWORD_INPUT, password)
        if age:
            self.input_text(self.AGE_INPUT, age)
        if birthday:
            self.input_text(self.BIRTHDAY_INPUT, birthday)
        if country:
            self.select_country(country)
        if gender:
            self.select_gender(gender)
        if hobbies:
            self.select_hobbies(hobbies)
        if description:
            self.input_text(self.DESCRIPTION_TEXTAREA, description)
        return self

    def select_country(self, value):
        """选择国家"""
        self.click(self.COUNTRY_SELECT)
        option = (By.XPATH, f"//select[@id='country']/option[@value='{value}']")
        self.click(option)

    def select_gender(self, gender):
        """选择性别"""
        gender_map = {"male": self.MALE_RADIO, "female": self.FEMALE_RADIO, "other": self.OTHER_RADIO}
        if gender in gender_map:
            self.click(gender_map[gender])

    def select_hobbies(self, hobbies):
        """选择多个兴趣爱好"""
        hobby_map = {
            "reading": self.HOBBY_READING,
            "sports": self.HOBBY_SPORTS,
            "music": self.HOBBY_MUSIC,
            "travel": self.HOBBY_TRAVEL
        }
        for hobby in hobbies:
            if hobby in hobby_map:
                self.click(hobby_map[hobby])

    def submit_form(self):
        """提交表单"""
        self.click(self.FORM_SUBMIT_BTN)

    def reset_form(self):
        """重置表单"""
        self.click(self.FORM_RESET_BTN)

    def click_button(self, btn_type):
        """点击按钮"""
        btn_map = {
            "primary": self.BTN_PRIMARY,
            "success": self.BTN_SUCCESS,
            "danger": self.BTN_DANGER,
            "warning": self.BTN_WARNING,
            "open_modal": self.BTN_OPEN_MODAL,
            "show_loading": self.BTN_SHOW_LOADING
        }
        if btn_type in btn_map:
            self.click(btn_map[btn_type])

    def open_modal(self):
        """打开弹窗"""
        self.click(self.BTN_OPEN_MODAL)

    def close_modal(self):
        """关闭弹窗"""
        self.click(self.MODAL_CLOSE_BTN)

    def click_modal_outside(self):
        """点击弹窗外部关闭"""
        self.driver.switch_to.active_element
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).move_to_element(self.find_element(self.MODAL)).click().perform()

    def switch_tab(self, tab_num):
        """切换标签页 1/2/3"""
        tab_map = {1: self.TAB_1, 2: self.TAB_2, 3: self.TAB_3}
        if tab_num in tab_map:
            self.click(tab_map[tab_num])

    def start_progress(self):
        """开始进度条"""
        self.click(self.BTN_START_PROGRESS)

    def reset_progress(self):
        """重置进度条"""
        self.click(self.BTN_RESET_PROGRESS)

    def upload_file(self, file_path):
        """上传文件"""
        self.find_element(self.FILE_INPUT).send_keys(file_path)

    def get_table_row_count(self):
        """获取表格行数"""
        return len(self.find_elements(self.TABLE_ROWS))

    def get_table_data(self):
        """获取表格所有数据"""
        rows = self.find_elements(self.TABLE_ROWS)
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            data.append([cell.text for cell in cells[:-1]])  # 排除操作列
        return data

    def click_edit_button(self, row_index):
        """点击指定行的编辑按钮"""
        edit_btns = self.find_elements(self.EDIT_BTNS)
        if 0 <= row_index < len(edit_btns):
            edit_btns[row_index].click()
