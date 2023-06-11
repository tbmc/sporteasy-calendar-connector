FROM python:3.11.4-slim-bullseye

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
