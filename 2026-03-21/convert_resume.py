import markdown

with open('D:/AI_Files/2026-03-21/徐宁波-软件测试工程师-简历-优化版.md', 'r', encoding='utf-8') as f:
    html = markdown.markdown(f.read())

styled_html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { font-family: Microsoft YaHei, sans-serif; margin: 40px; line-height: 1.6; color: #333; }
h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
h2 { color: #34495e; margin-top: 30px; }
ul { padding-left: 20px; }
li { margin: 5px 0; }
</style>
</head>
<body>
''' + html + '''
</body>
</html>
'''

with open('D:/AI_Files/2026-03-21/简历.html', 'w', encoding='utf-8') as f:
    f.write(styled_html)

print('HTML created successfully!')
