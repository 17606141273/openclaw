#!/usr/bin/env python3
"""
本地文件服务器 - 带密码保护
宁用这个在本地架一个文件站，通过Cloudflare Tunnel从外网访问
"""

import http.server
import socketserver
import os
import hashlib
import base64
import urllib.parse

PORT = 8080
USERNAME = "ning"
PASSWORD = "2026ning"  # 账号:ning  密码:2026ning

AUTH_HEADERS = {
    'WWW-Authenticate': 'Basic realm="文件站 - 请输入账号密码"',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
}

HTML_HEADER = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>文件站 | {path}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Segoe UI',sans-serif; background:#0f0f1a; color:#e0e0e0; min-height:100vh; }}
.header {{ background:#1a1a2e; padding:20px 30px; border-bottom:2px solid #00e5ff; display:flex; align-items:center; gap:15px; }}
.header h1 {{ color:#00e5ff; font-size:22px; }}
.header span {{ color:#888; font-size:13px; }}
.content {{ padding:20px 30px; }}
.path-bar {{ background:#1a1a2e; padding:12px 20px; border-radius:8px; margin-bottom:20px; font-size:13px; color:#aaa; word-break:break-all; }}
.path-bar a {{ color:#00e5ff; text-decoration:none; margin-right:5px; }}
.path-bar a:hover {{ text-decoration:underline; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:15px; }}
.card {{ background:#1a1a2e; border:1px solid #2a2a4a; border-radius:12px; padding:18px; transition:all 0.2s; cursor:pointer; text-decoration:none; display:block; color:#e0e0e0; }}
.card:hover {{ border-color:#00e5ff; transform:translateY(-2px); box-shadow:0 4px 20px rgba(0,229,255,0.1); }}
.card .icon {{ font-size:36px; margin-bottom:10px; }}
.card .name {{ font-size:14px; font-weight:600; word-break:break-all; margin-bottom:6px; }}
.card .meta {{ font-size:12px; color:#888; }}
.card.folder {{ border-color:#9b59b6; }}
.card.folder:hover {{ border-color:#bb00ff; box-shadow:0 4px 20px rgba(187,0,255,0.15); }}
.empty {{ text-align:center; padding:60px; color:#666; font-size:15px; }}
footer {{ text-align:center; padding:20px; color:#444; font-size:12px; border-top:1px solid #1a1a2e; margin-top:40px; }}
</style>
</head>
<body>
<div class="header">
  <h1>📁 文件站</h1>
  <span>宁的私人文件浏览</span>
</div>
<div class="content">
"""

HTML_FOOTER = """
</div>
<footer>Powered by Python HTTP Server + Cloudflare Tunnel</footer>
</body>
</html>
"""

def get_file_icon(name, is_dir):
    if is_dir:
        return "📁"
    ext = os.path.splitext(name)[1].lower()
    icons = {
        '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.webp': '🖼️',
        '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬', '.mov': '🎬',
        '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵',
        '.pdf': '📕', '.doc': '📄', '.docx': '📄', '.xls': '📊', '.xlsx': '📊',
        '.ppt': '📋', '.pptx': '📋',
        '.zip': '🗜️', '.rar': '🗜️', '.7z': '🗜️', '.tar': '🗜️',
        '.txt': '📝', '.md': '📝',
        '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨',
        '.exe': '⚙️', '.dll': '⚙️',
    }
    return icons.get(ext, '📄')

def format_size(size):
    if size < 1024:
        return f"{size}B"
    elif size < 1024*1024:
        return f"{size/1024:.1f}KB"
    elif size < 1024*1024*1024:
        return f"{size/1024/1024:.1f}MB"
    else:
        return f"{size/1024/1024/1024:.2f}GB"

def get_parent_path(path):
    parts = path.strip('/').split('/')
    if len(parts) <= 1:
        return "/"
    return "/".join(parts[:-1]) or "/"

def serve_path(path, rel_path):
    """生成目录列表HTML"""
    abs_path = os.path.join(os.getcwd(), rel_path.strip('/'))
    if not os.path.exists(abs_path):
        return f"<p class='empty'>路径不存在: {rel_path}</p>"

    entries = []
    if rel_path != "/":
        parent = get_parent_path(rel_path)
        entries.append({
            'type': 'parent',
            'name': '..',
            'link': parent,
            'size': '',
            'mtime': ''
        })

    try:
        items = sorted(os.listdir(abs_path), key=lambda x: (not os.path.isdir(os.path.join(abs_path, x)), x.lower()))
    except PermissionError:
        return f"<p class='empty'>没有权限访问此目录</p>"

    for name in items:
        item_rel = f"{rel_path.rstrip('/')}/{name}"
        item_abs = os.path.join(abs_path, name)
        try:
            is_dir = os.path.isdir(item_abs)
            size = "" if is_dir else format_size(os.path.getsize(item_abs))
            mtime = ""
        except:
            continue

        icon = get_file_icon(name, is_dir)
        if is_dir:
            entries.append({
                'type': 'folder',
                'name': name,
                'link': item_rel,
                'size': '文件夹',
                'mtime': mtime
            })
        else:
            encoded = urllib.parse.quote(item_rel)
            entries.append({
                'type': 'file',
                'name': name,
                'link': f"/download{encoded}",
                'size': size,
                'mtime': mtime
            })

    crumbs = ['<a href="/">/</a>']
    if rel_path != "/":
        parts = rel_path.strip('/').split('/')
        cum_path = ""
        for p in parts:
            cum_path += "/" + p
            crumbs.append(f'<a href="{cum_path}">{p}/</a>')

    path_html = "".join(crumbs)

    cards_html = ""
    for item in entries:
        if item['type'] == 'parent':
            cards_html += f"""
    <a href="{item['link']}" class="card folder">
      <div class="icon">⬆️</div>
      <div class="name">上级目录</div>
      <div class="meta">..</div>
    </a>"""
        elif item['type'] == 'folder':
            cards_html += f"""
    <a href="{item['link']}" class="card folder">
      <div class="icon">{icon}</div>
      <div class="name">{item['name']}</div>
      <div class="meta">文件夹</div>
    </a>"""
        else:
            cards_html += f"""
    <a href="{item['link']}" class="card">
      <div class="icon">{icon}</div>
      <div class="name">{item['name']}</div>
      <div class="meta">{item['size']}</div>
    </a>"""

    if not cards_html:
        cards_html = '<p class="empty">此目录为空</p>'

    return f"""
  <div class="path-bar">位置: {path_html}</div>
  <div class="grid">{cards_html}</div>
"""

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

    def do_HEAD(self):
        self.send_response(401)
        self.send_header('Content-Type', 'text/html')
        for k, v in AUTH_HEADERS.items():
            self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        if not self.authenticate():
            self.send_response(401)
            for k, v in AUTH_HEADERS.items():
                self.send_header(k, v)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Unauthorized</h1>')
            return

        path = urllib.parse.unquote(self.path)

        if path.startswith('/download'):
            file_path = path[len('/download'):].lstrip('/')
            file_abs = os.path.join(os.getcwd(), file_path)
            if os.path.isfile(file_abs):
                self.send_response(200)
                filename = os.path.basename(file_path)
                self.send_header('Content-Disposition', f'attachment; filename*=UTF-8\'\'{urllib.parse.quote(filename)}')
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', os.path.getsize(file_abs))
                self.end_headers()
                with open(file_abs, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.wfile.write(b'File not found')
                return

        if path == '/':
            self.path = '/'

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def authenticate(self):
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Basic '):
            return False
        try:
            encoded = auth_header[6:]
            decoded = base64.b64decode(encoded).decode('utf-8')
            user, pw = decoded.split(':', 1)
            return user == USERNAME and pw == PASSWORD
        except:
            return False

    def list_directory(self, path):
        path = urllib.parse.unquote(self.path)
        if path == '/':
            rel_path = '/'
        else:
            rel_path = path

        enc_path = urllib.parse.quote(path)
        body = (
            HTML_HEADER.format(path=rel_path) +
            serve_path(path, rel_path) +
            HTML_FOOTER
        )
        body = body.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)
        return None

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    print("="*50)
    print("📁 本地文件站启动中...")
    print(f"📍 访问地址: http://localhost:{PORT}")
    print(f"🔐 账号: {USERNAME}")
    print(f"🔐 密码: {PASSWORD}")
    print()
    print("⚠️  重要: 需要先安装 cloudflared 来穿透外网")
    print("   下载: https://github.com/cloudflare/cloudflared/releases")
    print("   安装后运行: cloudflared tunnel --url http://localhost:8080")
    print("   会给你一个公网URL，在外网就能访问了！")
    print("="*50)

    os.chdir(os.path.expanduser("~"))
    print(f"📂 文件根目录: {os.getcwd()}")

    with socketserver.TCPServer(("", PORT), AuthHandler) as httpd:
        print(f"🚀 服务已启动 http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 服务已关闭")
