import subprocess, sys, os, time, urllib.request

BASE = r"D:\HuaweiMoveData\Users\Anna\Documents\星云学\星学堂"
os.chdir(BASE)

def start_django():
    """用 cmd /c start /B 可靠启动"""
    python = r"..\.venv\Scripts\python.exe"
    proc = subprocess.Popen(
        ['cmd.exe', '/c', 'start', '/B', python, 'manage.py', 'runserver', '0.0.0.0:8000'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    for i in range(15):
        try:
            r = urllib.request.urlopen('http://127.0.0.1:8000/api/health/', timeout=2)
            if r.status == 200: print('Django OK!'); return True
        except: pass
        time.sleep(1)
    print('Django 启动失败')
    return False

def start_tunnel():
    """启动 localtunnel"""
    lt = os.path.expanduser('~') + '/AppData/Roaming/npm/lt.cmd'
    if not os.path.exists(lt): print('localtunnel 未安装'); return None
    proc = subprocess.Popen(
        ['cmd.exe', '/c', lt, '--port', '8000'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    time.sleep(4)
    try:
        out = proc.stdout.read(2048).decode('utf-8', errors='ignore')
        for line in out.split('\n'):
            if 'your url is:' in line:
                url = line.split(': ', 1)[1].strip()
                print(f'公网: {url}')
                print(f'闯关: {url}/checkin/')
                return url
    except: pass
    return None

if __name__ == '__main__':
    print('=== 星学堂启动 ===')
    if start_django():
        r = urllib.request.urlopen('http://127.0.0.1:8000/checkin/')
        print(f'闯关: {r.status}')
        r2 = urllib.request.urlopen('http://127.0.0.1:8000/admin/login/?next=/admin/')
        print(f'后台: {r2.status}')
        url = start_tunnel()
        print(f'\n本地: http://127.0.0.1:8000/')
        print(f'后台: http://127.0.0.1:8000/admin/')
