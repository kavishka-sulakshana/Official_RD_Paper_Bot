FROM python:3.11.6-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

RUN useradd -ms /bin/sh tele-user
USER tele-user

ENV DOCKER_HOST=unix:///var/run/docker.sock

RUN setfacl -d /root:tele-user
RUN setfacl -d /var/run/docker.sock:tele-user

EXPOSE 8443

CMD ["python", "bot.py"]
