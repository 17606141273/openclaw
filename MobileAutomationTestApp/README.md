# MobileAutomationTestApp

这是一个专门用于移动端自动化测试练习的 Android 应用。

## 功能特性

- 登录页面（包含各种输入验证）
- 列表页面（支持下拉刷新、上拉加载）
- 轮播图组件
- 底部导航栏
- 侧边抽屉菜单
- 表单页面（包含各种输入控件）
- WebView 页面
- 弹窗和对话框
- 手势操作区域

## 如何编译

1. 安装 Android Studio
2. 打开本项目
3. 同步 Gradle
4. Build -> Build Bundle(s) / APK(s) -> Build APK(s)

## 项目结构

```
app/
├── src/main/java/com/example/automationtest/
│   ├── MainActivity.java
│   ├── LoginActivity.java
│   ├── ListActivity.java
│   ├── FormActivity.java
│   ├── WebViewActivity.java
│   └── GestureActivity.java
├── src/main/res/layout/
│   └── (布局文件)
└── src/main/res/values/
    └── (资源文件)
```

## 测试建议

- 使用 Appium 进行 UI 自动化测试
- 使用 Espresso 进行原生测试
- 使用 UI Automator 进行跨应用测试