FROM python:3.11.6-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8443

CMD ["python", "bot.py"]
