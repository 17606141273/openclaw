import os

code = '''#!/usr/bin/env python3
import http.server, socketserver, os, base64, urllib.parse

PORT = 8080
USERNAME = "ning"
PASSWORD = "2026ning"
ROOT = os.path.expanduser("~")

AUTH_HEADERS = {'WWW-Authenticate': 'Basic realm="File Server"', 'X-Frame-Options': 'DENY'}

HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>File Station</title>
<style>body{font-family:Segoe UI;background:#0f0f1a;color:#e0e0e0;margin:0;padding:20px}
h1{color:#00e5ff;border-bottom:2px solid #00e5ff;padding-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.card{background:#1a1a2e;border:1px solid #2a2a4a;border-radius:10px;padding:15px;text-decoration:none;color:#e0e0e0;display:block}
.card:hover{border-color:#00e5ff;transform:translateY(-2px)}
.icon{font-size:28px;margin-bottom:8px}.name{font-size:13px;word-break:break-all}
.meta{font-size:11px;color:#888;margin-top:5px}
.path{background:#1a1a2e;padding:10px 15px;border-radius:6px;margin-bottom:20px;font-size:12px;color:#888}
.footer{text-align:center;margin-top:40px;color:#444;font-size:12px}
</style></head><body><h1>File Station</h1><div class="path">%PATH%</div><div class="grid">%ITEMS%</div><div class="footer">Powered by Python</div></body></html>"""

def icon(name, is_dir):
    if is_dir: return "Folder"
    ext = os.path.splitext(name)[1].lower()
    m = {'.jpg':'Image','.png':'Image','.gif':'Image','.pdf':'PDF','.mp4':'Video','.mp3':'Audio','.zip':'Archive','.txt':'Text'}
    return m.get(ext, 'File')

def size_fmt(s):
    for u,b in [('',1),('KB',1024),('MB',1024**2),('GB',1024**3)]:
        if s<1024: return f"{s:.1f}{u}"
        s/=1024
    return f"{s:.1f}GB"

def list_dir(path):
    items = []
    if path != '/':
        parent = '/'.join(path.strip('/').split('/')[:-1]) or '/'
        items.append(('parent','..',parent,''))
    try:
        for n in sorted(os.listdir(ROOT+path), key=lambda x: (not os.path.isdir(os.path.join(ROOT+path,x)), x.lower())):
            fp = os.path.join(ROOT+path, n)
            is_dir = os.path.isdir(fp)
            sz = '' if is_dir else size_fmt(os.path.getsize(fp))
            items.append(('file' if not is_dir else 'folder', n, path.rstrip('/')+'/'+n, sz))
    except: pass
    return items

def render(path):
    path_escaped = ''.join(f'<a href="/{p}">{p}/</a>' for p in ['']+path.strip('/').split('/'))
    items = list_dir(path)
    cards = ''
    for typ, name, link, sz in items:
        if typ == 'parent':
            cards += f'<a href="/{link}" class="card"><div class="icon">Up</div><div class="name">..</div></a>'
        else:
            cards += f'<a href="/{link}" class="card"><div class="icon">{icon(name, typ=="folder")}</div><div class="name">{name}</div><div class="meta">{sz}</div></a>'
    return HTML.replace('%PATH%', path_escaped).replace('%ITEMS%', cards or '<p style="color:#888;text-align:center;padding:40px">Empty</p>')

class H(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(401)
        for k,v in AUTH_HEADERS.items(): self.send_header(k,v)
        self.end_headers()
    def do_GET(self):
        if not self.auth():
            self.send_response(401)
            for k,v in AUTH_HEADERS.items(): self.send_header(k,v)
            self.end_headers()
            self.wfile.write(b'<h1>401 Unauthorized</h1>')
            return
        path = urllib.parse.unquote(self.path)
        if path == '/': path = '/'
        if path.startswith('/download/'):
            fp = os.path.join(ROOT, path[10:].lstrip('/'))
            if os.path.isfile(fp):
                self.send_response(200)
                self.send_header('Content-Disposition', 'attachment; filename*=UTF-8')
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', os.path.getsize(fp))
                self.end_headers()
                with open(fp,'rb') as f: self.wfile.write(f.read())
                return
        http.server.SimpleHTTPRequestHandler.do_GET(self)
    def auth(self):
        h = self.headers.get('Authorization','')
        if not h.startswith('Basic '): return False
        try:
            u,p = base64.b64decode(h[6:]).decode().split(':',1)
            return u==USERNAME and p==PASSWORD
        except: return False
    def log_message(self, s, *a): print('[' + self.log_date_time_string() + '] ' + (s % a))
    def list_directory(self, path):
        path = urllib.parse.unquote(self.path)
        body = render(path).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)
        return None

print(f'Starting server on port {PORT}...')
print(f'Root: {ROOT}')
print(f'URL: http://localhost:{PORT}')
print(f'User: {USERNAME}, Password: {PASSWORD}')
os.chdir(ROOT)
with socketserver.TCPServer(('', PORT), H) as httpd:
    print(f'Serving on port {PORT}')
    httpd.serve_forever()
'''

target_dir = r'D:\AI_Files\server'
os.makedirs(target_dir, exist_ok=True)
file_path = os.path.join(target_dir, 'file_server.py')
print(f"Writing to: {file_path}")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print('File written successfully')
