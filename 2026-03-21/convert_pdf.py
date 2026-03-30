from weasyprint import HTML
import markdown

# Convert MD to HTML
with open('D:/AI_Files/2026-03-21/徐宁波-软件测试工程师-简历-优化版.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

html_content = markdown.markdown(md_content)

# Add styling
styled_html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: Microsoft YaHei, sans-serif; margin: 40px; line-height: 1.6; color: #333; max-width: 800px; }}
h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
h2 {{ color: #34495e; margin-top: 25px; background: #ecf0f1; padding: 8px 15px; border-radius: 5px; }}
h3 {{ color: #7f8c8d; }}
ul {{ padding-left: 25px; }}
li {{ margin: 5px 0; }}
p {{ margin: 10px 0; }}
</style>
</head>
<body>
{html_content}
</body>
</html>
'''

# Convert to PDF
HTML(string=styled_html).write_pdf('D:/AI_Files/2026-03-21/徐宁波-简历-优化版.pdf')

print('PDF created successfully!')
