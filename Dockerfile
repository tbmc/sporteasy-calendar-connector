FROM python:3.11.4-slim-bullseye

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "flask run"]
