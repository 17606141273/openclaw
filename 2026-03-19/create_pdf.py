from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# 创建PDF
pdf_path = r'D:\AI_Files\2026-03-19\徐宁波-简历-优化版.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)

# 样式
styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=18, alignment=TA_CENTER, spaceAfter=10)
heading_style = ParagraphStyle('Heading', parent=styles['Heading1'], fontSize=14, spaceAfter=6, spaceBefore=12, textColor=colors.HexColor('#2c5aa0'))
subheading_style = ParagraphStyle('SubHeading', parent=styles['Heading2'], fontSize=12, spaceAfter=4, spaceBefore=8)
normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, spaceAfter=4, leading=14)

# 内容
story = []

# 标题
story.append(Paragraph('徐宁波 | 软件测试工程师', title_style))
story.append(Spacer(1, 5*mm))

# 基本信息
info_text = '<b>电话：</b>17633887100  |  <b>邮箱：</b>bobo1273@163.com  |  <b>现居：</b>长沙市  |  <b>求职意向：</b>杭州 · 软件测试/自动化测试工程师'
story.append(Paragraph(info_text, normal_style))
story.append(Spacer(1, 5*mm))

# 工作经历
story.append(Paragraph('工作经历', heading_style))

story.append(Paragraph('<b>杭州七凌科技有限公司（字节跳动/抖音项目）｜软件测试工程师</b>', subheading_style))
story.append(Paragraph('<i>2024.7 – 至今</i>', normal_style))
story.append(Paragraph('• 负责抖音增长业务（青少年、投放承接、桌面组件）质量保障，支撑产品快速迭代与稳定上线', normal_style))
story.append(Paragraph('• 基于Tesla平台搭建接口自动化测试体系，编写并维护用例库，替代80%重复手动回归工作', normal_style))
story.append(Paragraph('• 使用Shoots+Python实现抖音及同构版整体投放链路UI自动化，覆盖Android/iOS全版本，用例通过率稳定在95%+', normal_style))
story.append(Paragraph('• 基于Kepler平台完成全链路监控接入与异常检测，精准识别大促场景服务异常', normal_style))
story.append(Paragraph('• 通过混沌平台模拟极端场景，验证系统容错与故障恢复能力', normal_style))
story.append(Paragraph('• 规范Bug记录与生命周期管理，推动Bug高效闭环', normal_style))

story.append(Spacer(1, 3*mm))

story.append(Paragraph('<b>博彦科技股份有限公司（Automation Team）｜自动化测试工程师</b>', subheading_style))
story.append(Paragraph('<i>2021.7 – 2024.3</i>', normal_style))
story.append(Paragraph('• 主导设计并落地基于Python+Selenium的Web端自动化测试框架，核心测试覆盖率85%+', normal_style))
story.append(Paragraph('• 基于Jenkins搭建CI/CD自动化测试流水线，实现测试脚本自动触发、执行及报告自动输出', normal_style))
story.append(Paragraph('• 独立搭建性能测试体系，运用JMeter模拟高并发场景，使平台高峰期响应时间缩短50%', normal_style))
story.append(Paragraph('• 使用Jira进行缺陷全生命周期管理，推动问题高效闭环', normal_style))

# 专业技能
story.append(Paragraph('专业技能', heading_style))

skills_data = [
    ['类别', '技能'],
    ['自动化测试', 'Selenium + Python + Pytest + Yaml + POM 搭建Web UI自动化框架'],
    ['接口测试', 'Requests + Pytest + Allure 接口自动化，Tesla 框架全流程落地'],
    ['性能测试', 'JMeter 脚本创建、场景设置、报告分析及瓶颈定位'],
    ['持续集成', 'Jenkins 持续集成、自动部署、定时任务配置'],
    ['测试工具', '禅道、Meego、Jira、Git、MySQL、Linux'],
    ['平台经验', '字节跳动 Kepler 智能运维平台、Shoots、BitS、混沌平台'],
]

table = Table(skills_data, colWidths=[80*mm, 90*mm])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('PADDING', (0, 0), (-1, -1), 4),
]))
story.append(table)

# 项目经历
story.append(Paragraph('项目经历', heading_style))

story.append(Paragraph('<b>抖音UG投放拉活用户厂商位置定制策略｜项目QA</b>', subheading_style))
story.append(Paragraph('<i>2025.7-2025.10</i>', normal_style))
story.append(Paragraph('• 深度解读需求文档与接口文档，拆解厂商适配规则与用户分层触达条件', normal_style))
story.append(Paragraph('• 主导多厂商手机（华为、小米、OPPO、vivo等）及不同系统版本的兼容性测试', normal_style))
story.append(Paragraph('• 基于Tesla平台编写接口自动化用例，与功能测试同步进行，测试效率提升60%', normal_style))
story.append(Paragraph('• 利用GUI智能测试平台验证埋点数据，缩短70%测试时间', normal_style))
story.append(Paragraph('• 编写自动化脚本覆盖约80%核心回归用例，提升集成回归效率', normal_style))

story.append(Spacer(1, 3*mm))

story.append(Paragraph('<b>抖音UG投放承接项目｜项目QA</b>', subheading_style))
story.append(Paragraph('<i>2024.7 – 至今</i>', normal_style))
story.append(Paragraph('• 负责用户从端外广告点击到进端的整体流程测试，保障"所见即所得"', normal_style))
story.append(Paragraph('• 基于Tesla平台实现接口自动化，高效消费测试结果', normal_style))
story.append(Paragraph('• 利用GUI智能测试平台对庞大埋点数据进行验证，提前规避多处问题', normal_style))
story.append(Paragraph('• 通过BitS平台设置每周定时巡检，避免版本迭代引入回归Bug', normal_style))

# 教育背景
story.append(Paragraph('教育背景', heading_style))
story.append(Paragraph('宿迁职业技术学院 ｜ 移动应用开发 ｜ 专科（2020.10 – 2023.7）', normal_style))

# 自我评价
story.append(Paragraph('自我评价', heading_style))
story.append(Paragraph('具备4年互联网软件测试实战经验，熟悉敏捷迭代流程，精通功能、兼容性、接口、性能及自动化全维度测试。擅长自动化框架搭建与CI/CD落地，注重测试效率与质量保障，能快速定位问题并沉淀测试方案，以严谨的测试思维保障产品稳定上线与迭代优化。', normal_style))

# 生成PDF
doc.build(story)
print(f'PDF生成成功！路径：{pdf_path}')
