import json
data = {
    "build": {
        "builder": "NIXPACKS",
        "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput"
    },
    "deploy": {
        "startCommand": "gunicorn nebula.wsgi --bind 0.0.0.0:D_PORT",
        "restartPolicyType": "ON_FAILURE"
    }
}
text = json.dumps(data, indent=2, ensure_ascii=False)
text = text.replace('D_PORT', '')
with open('D:\\HuaweiMoveData\\Users\\Anna\\Documents\\星云学\\星学堂\\railway.json', 'w', encoding='utf-8') as f:
    f.write(text)
print('OK:', text[:100])
