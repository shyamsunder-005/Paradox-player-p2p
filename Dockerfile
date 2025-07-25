FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app/main.py", "--server.port=8080", "--server.enableCORS=false"]
