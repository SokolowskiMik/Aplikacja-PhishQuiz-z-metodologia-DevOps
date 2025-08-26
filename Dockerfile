FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /app

ARG DJANGO_SECRET_KEY=dummy-secret-key-for-building
ENV SECRET_KEY=$DJANGO_SECRET_KEY
RUN python manage.py collectstatic --no-input

USER app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]