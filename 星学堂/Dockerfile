FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /app/frontend
RUN npm install && npm run build
WORKDIR /app
RUN python manage.py collectstatic --noinput 2>/dev/null || true
ENV PORT=8080
EXPOSE ${PORT:-8080}
CMD python manage.py migrate --run-syncdb 2>/dev/null; python manage.py createsuperuser --noinput 2>/dev/null; gunicorn nebula.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120
