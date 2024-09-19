FROM python:3.12

WORKDIR /app

COPY ./app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD if [ "$MIGRATE" = "true" ]; then alembic revision --autogenerate && alembic upgrade head; fi && \
    uvicorn main:app --host 0.0.0.0 --port 8000
