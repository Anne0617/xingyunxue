import subprocess, time, urllib.request, os, sys, re

BASE = r"D:\HuaweiMoveData\Users\Anna\Documents\星云学\星学堂"
PYTHON = r"D:\HuaweiMoveData\Users\Anna\Documents\星云学\.venv\Scripts\python.exe"
os.chdir(BASE)

def start_django():
    proc = subprocess.Popen(
        [PYTHON, 'manage.py', 'runserver', '0.0.0.0:8000'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=subprocess.DETACHED_PROCESS
    )
    for i in range(15):
        try:
            r = urllib.request.urlopen('http://127.0.0.1:8000/api/health/', timeout=2)
            if r.status == 200: return True
        except: pass
        time.sleep(1)
    return False

def start_tunnel():
    lt = os.path.expanduser('~') + r'\AppData\Roaming\npm\node_modules\localtunnel\bin\lt.js'
    node = os.path.expanduser('~') + r'\AppData\Roaming\npm\node_modules\node\bin\node.exe'
    if not os.path.exists(node): node = 'node'
    
    # 启动 lt 并捕获输出
    proc = subprocess.Popen(
        [node, lt, '--port', '8000'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    
    # 读第一行输出（URL）
    url = None
    for _ in range(20):
        if proc.poll() is not None: break
        import msvcrt, msvcrt
        try:
            line = proc.stdout.readline().decode('utf-8', errors='ignore').strip()
            if 'your url is:' in line:
                url = line.split('your url is: ')[-1].strip()
                break
        except: pass
        time.sleep(1)
    
    if url: return url, proc
    return None, proc

print('=== 星学堂启动 ===')
print('[1/3] 启动 Django...')
if start_django():
    print('  Django OK!')
    print('[2/3] 启动公网隧道...')
    url, p = start_tunnel()
    if url:
        print(f'  公网地址: {url}')
        print(f'  闯关游戏: {url}/checkin/')
        print(f'  推广页面: {url}/checkin/promo/')
        print(f'  管理后台: {url}/admin/')
        print('[3/3] 验证公网访问...')
        time.sleep(2)
        checkin = urllib.request.urlopen(url + '/checkin/', timeout=5)
        m = re.search(r'<title>(.*?)</title>', checkin.read().decode())
        t = m.group(1) if m else 'none'
        print(f'  {checkin.status} {url}/checkin/ - {t}')
    else:
        print('  隧道启动超时')
else:
    print('  Django 启动失败')

print(f'\n本地地址: http://127.0.0.1:8000/')
print(f'闯关游戏: http://127.0.0.1:8000/checkin/')
print(f'管理后台: http://127.0.0.1:8000/admin/')
