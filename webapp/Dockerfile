FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /myapp

COPY requirements.txt .

RUN pip install --default-timeout=1000 --retries 10 -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]