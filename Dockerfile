FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*
COPY 星学堂/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY 星学堂/ .
WORKDIR /app/frontend
RUN npm install && npm run build
WORKDIR /app
RUN python manage.py collectstatic --noinput || true
ENV PORT=8080
EXPOSE ${PORT:-8080}
CMD set -x; python manage.py migrate --run-syncdb 2>&1; echo "=== migration done ==="; python manage.py createsuperuser --noinput 2>&1; echo "=== superuser done ==="; exec gunicorn nebula.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile -
