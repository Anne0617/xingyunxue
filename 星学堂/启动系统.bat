@echo off
cd /d D:\HuaweiMoveData\Users\Anna\Documents\星云学\星学堂
echo ========== 星学堂启动系统 ==========
echo.

:: 启动 Django 服务（后台运行）
echo [1/3] 启动 Django 服务...
start /B ..\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
timeout /t 5 /nobreak >nul

:: 检查服务是否启动
..\.venv\Scripts\python.exe -c "import urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8000/api/health/', timeout=3); print('      Django: OK' if r.status==200 else '      Django: FAIL')" 2>nul

:: 启动公网隧道（可选）
echo [2/3] 尝试启动公网隧道...
start /B lt --port 8000
timeout /t 5 /nobreak >nul

echo.
echo ========== 访问地址 ==========
echo.
echo  本地访问: http://127.0.0.1:8000/
echo  闯关游戏: http://127.0.0.1:8000/checkin/
echo  管理后台: http://127.0.0.1:8000/admin/
echo.
echo  管理账号: 星河智善总部 / xhzs2026
echo.
echo  如果隧道启动成功，会输出公网地址
echo ==============================
echo.
pause
