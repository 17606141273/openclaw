# 🧪 Automation Test Project (PO Model)

> 使用 Python + Selenium + Pytest + Page Object 模型的自动化测试项目

## 📁 项目结构

```
automation_test/
├── pages/                    # 页面对象目录
│   ├── __init__.py
│   ├── base_page.py         # 基础页面对象（封装公共操作）
│   └── home_page.py         # 首页页面对象（页面特有元素和操作）
├── testcases/               # 测试用例目录
│   ├── __init__.py
│   ├── conftest.py          # pytest 配置和 fixture
│   ├── test_form.py         # 表单测试用例
│   ├── test_button.py       # 按钮和弹窗测试用例
│   └── test_widgets.py      # 进度条、标签页、表格、上传测试
├── screenshots/             # 截图目录（自动创建）
│   └── failed/              # 失败截图
├── requirements.txt         # 依赖
└── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 确保 Chrome 浏览器已安装

项目使用 Chrome WebDriver，请确保：
- Chrome 浏览器已安装
- ChromeDriver 匹配你的 Chrome 版本（Selenium 4+ 会自动管理）

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest testcases/test_form.py

# 运行指定测试类
pytest testcases/test_form.py::TestForm

# 运行指定测试方法
pytest testcases/test_form.py::TestForm::test_fill_and_submit_form

# 显示详细输出
pytest -v

# 显示打印内容
pytest -s

# 生成 HTML 报告
pytest --html=reports/report.html --self-contained-html

# 并行执行（加速）
pytest -n auto
```

## 📝 测试用例说明

### test_form.py - 表单测试
| 用例 | 说明 |
|------|------|
| `test_page_title` | 验证页面标题 |
| `test_form_elements_visible` | 验证表单元素可见 |
| `test_fill_and_submit_form` | 填写并提交表单 |
| `test_form_validation_required_fields` | 表单必填项验证 |
| `test_gender_selection` | 性别单选框测试 |
| `test_hobby_multi_select` | 兴趣爱好多选测试 |
| `test_country_dropdown` | 国家下拉框测试 |
| `test_form_reset` | 表单重置功能测试 |
| `test_birthday_input` | 日期输入测试 |
| `test_age_input` | 年龄输入测试 |

### test_button.py - 按钮和弹窗测试
| 用例 | 说明 |
|------|------|
| `test_buttons_visible` | 验证按钮可见 |
| `test_primary_button_click` | 主要按钮点击 |
| `test_success_button_click` | 成功按钮点击 |
| `test_danger_button_click` | 危险按钮点击 |
| `test_warning_button_click` | 警告按钮点击 |
| `test_open_modal` | 打开弹窗 |
| `test_modal_content` | 弹窗内容验证 |
| `test_close_modal_by_button` | 点击按钮关闭弹窗 |
| `test_close_modal_by_outside` | 点击外部关闭弹窗 |
| `test_modal_reopen` | 弹窗重新打开 |

### test_widgets.py - 组件测试
| 用例 | 说明 |
|------|------|
| `test_progress_bar_visible` | 进度条可见 |
| `test_start_progress` | 开始进度条 |
| `test_progress_completes` | 进度条完成到100% |
| `test_reset_progress` | 重置进度条 |
| `test_tabs_visible` | 标签页可见 |
| `test_default_active_tab` | 默认激活标签页 |
| `test_switch_to_tab2` | 切换到标签页2 |
| `test_switch_to_tab3` | 切换到标签页3 |
| `test_tab_switching` | 标签页切换 |
| `test_table_visible` | 表格可见 |
| `test_table_headers` | 表格表头 |
| `test_table_row_count` | 表格行数 |
| `test_get_table_data` | 获取表格数据 |
| `test_edit_button_click` | 编辑按钮可点击 |
| `test_drop_zone_visible` | 上传区域可见 |
| `test_file_input_exists` | 文件输入框存在 |
| `test_upload_small_file` | 上传小文件 |
| `test_show_loading_button` | 显示加载按钮 |
| `test_loading_display` | 加载动画显示 |

## 📊 页面对象模型说明

### BasePage 封装的方法
- `find_element(locator)` - 查找单个元素
- `find_elements(locator)` - 查找多个元素
- `click(locator)` - 点击
- `input_text(locator, text)` - 输入文本
- `get_text(locator)` - 获取文本
- `get_attribute(locator, attr)` - 获取属性
- `is_element_visible(locator)` - 元素是否可见
- `is_element_clickable(locator)` - 元素是否可点击
- `wait_for_alert()` - 等待 alert
- `switch_to_frame(locator)` - 切换 iframe
- `scroll_into_view(locator)` - 滚动到元素可见
- `screenshot(name)` - 截图

### HomePage 封装的方法
- `fill_form(...)` - 填写表单
- `select_country(value)` - 选择国家
- `select_gender(gender)` - 选择性别
- `select_hobbies(hobbies)` - 选择爱好
- `submit_form()` - 提交表单
- `reset_form()` - 重置表单
- `open_modal()` / `close_modal()` - 打开/关闭弹窗
- `switch_tab(tab_num)` - 切换标签页
- `start_progress()` / `reset_progress()` - 进度条控制
- `upload_file(path)` - 文件上传
- `get_table_data()` - 获取表格数据

## 🔧 添加新页面对象

```python
# pages/new_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class NewPage(BasePage):
    ELEMENT_1 = (By.ID, "element1")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("url")
    
    def do_something(self):
        self.click(self.ELEMENT_1)
```

## ⚠️ 注意事项

1. 测试文件路径使用绝对路径指向 `D:\AI_Files\2026-03-21\automation-test-practice.html`
2. 如果文件路径不同，请修改 `home_page.py` 中的 URL
3. 失败截图会自动保存到 `screenshots/failed/` 目录
