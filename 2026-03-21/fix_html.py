import markdown

with open('D:/AI_Files/2026-03-21/徐宁波-软件测试工程师-简历-优化版.md', 'r', encoding='utf-8') as f:
    html = markdown.markdown(f.read(), extensions=['tables', 'fenced_code'])

styled = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; }
@page { margin: 1cm; @top-left { content: none; } @bottom-left { content: none; } @top-right { content: none; } @bottom-right { content: none; } }
body { font-family: Microsoft YaHei, sans-serif; margin: 0; padding: 40px; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; }
h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-top: 0; }
h2 { color: #34495e; margin-top: 25px; background: #ecf0f1; padding: 8px 15px; border-radius: 5px; font-size: 18px; }
h3 { color: #7f8c8d; }
ul { padding-left: 25px; }
li { margin: 5px 0; }
p { margin: 10px 0; }
hr { border: none; border-top: 1px solid #eee; margin: 20px 0; }
@media print { 
    @page { margin: 0.5cm; }
    body { padding: 0; }
    h1 { page-break-before: auto; }
    h2 { page-break-after: avoid; }
}
</style>
</head>
<body>
""" + html + """
</body>
</html>
"""

with open('D:/AI_Files/2026-03-21/徐宁波-简历.html', 'w', encoding='utf-8') as f:
    f.write(styled)

print("HTML updated without header/footer!")
