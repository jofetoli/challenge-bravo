FROM python:3.7
COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

EXPOSE 8080

COPY src /app/
COPY config /app/config/

WORKDIR /app

CMD [ "python3", "/app/app/server.py" ]