# UI Automation Test Project

基于 pytest + Selenium + Page Object Model 的 UI 自动化测试项目

## 项目结构

```
ui_automation_project/
├── pages/                  # 页面对象
│   ├── __init__.py
│   ├── base_page.py       # 基础页面对象
│   ├── form_page.py       # 表单页面
│   ├── button_page.py     # 按钮页面
│   ├── progress_page.py   # 进度条页面
│   ├── tab_page.py        # 标签页页面
│   ├── table_page.py      # 表格页面
│   └── file_upload_page.py # 文件上传页面
├── tests/                  # 测试用例
│   ├── __init__.py
│   ├── conftest.py        # pytest 配置和 fixtures
│   ├── test_form.py       # 表单测试
│   ├── test_button.py     # 按钮测试
│   ├── test_progress.py   # 进度条测试
│   ├── test_tab.py        # 标签页测试
│   ├── test_table.py      # 表格测试
│   ├── test_file_upload.py # 文件上传测试
│   └── test_integration.py # 集成测试
├── utils/                  # 工具类
│   ├── __init__.py
│   └── driver_factory.py  # 驱动工厂
├── reports/                # 测试报告
├── config/                 # 配置文件
└── requirements.txt        # 依赖文件
```

## 安装依赖

```bash
cd D:/AI_Files/ui_automation_project
pip install -r requirements.txt
```

## 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定模块
pytest tests/test_form.py -v
pytest tests/test_button.py -v

# 生成 HTML 报告
pytest tests/ --html=reports/report.html

# 运行带参数化测试
pytest tests/test_form.py::TestForm::test_select_country_options -v

# 并行运行测试（需要安装 pytest-xdist）
pytest tests/ -n auto
```

## 测试覆盖

| 模块 | 测试场景 | 用例数 |
|------|---------|--------|
| 表单 | 用户名、邮箱、密码、年龄、生日、国家、性别、爱好、简介、提交、重置、参数化测试 | 15+ |
| 按钮 | 主要/成功/危险/警告按钮、弹窗、加载动画 | 6 |
| 进度条 | 开始进度、完成验证、重置、进度增加 | 4 |
| 标签页 | 切换、内容验证、切换序列、可点击性 | 5 |
| 表格 | 行数、行数据、全部数据、查找、编辑、表头 | 6 |
| 文件上传 | 文本文件、文件信息、不同扩展名 | 3 |
| 集成测试 | 完整工作流程、错误处理、多操作序列 | 3 |

**总计：40+ 个测试用例**

## Page Object Model 设计

- **BasePage**: 封装通用方法（查找元素、点击、输入、等待等）
- **具体页面**: 继承 BasePage，定义页面特有的定位器和操作方法
- **Tests**: 使用 pytest fixtures 获取页面对象，编写测试用例

## 特点

- ✅ Page Object Model 设计模式
- ✅ pytest 测试框架
- ✅ 显式等待（WebDriverWait）
- ✅ 无头模式运行（可改有头）
- ✅ 参数化测试（@pytest.mark.parametrize）
- ✅ 临时文件自动清理
- ✅ 详细的测试断言
- ✅ 集成测试覆盖完整流程
- ✅ 驱动自动管理（webdriver-manager）
