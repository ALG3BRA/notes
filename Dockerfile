FROM python:3.12

WORKDIR /app

COPY ./app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

ENV PYTHONPATH=/app