FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install redis
RUN pip install flask

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]