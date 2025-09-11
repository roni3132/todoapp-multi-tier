FROM python:3.13 as builder

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

FROM python:3.13-slim-bookworm

WORKDIR /app


COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /app /app

EXPOSE 5000

CMD ["python", "app.py"]
