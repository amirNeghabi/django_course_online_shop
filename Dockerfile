FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# pip و setuptools قدیمی که با allauth 0.49.0 سازگار باشه
RUN pip install --upgrade pip setuptools==59.6.0 wheel

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
