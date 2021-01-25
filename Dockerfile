FROM python:3.7
COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

EXPOSE 8080

COPY src/app/ /app/
COPY src/integrations/ /app/integrations/
COPY src/infrastructure/ /app/infrastructure/

COPY config /app/config/

WORKDIR /app

RUN python3 -m pytest

CMD [ "python3", "/app/server.py" ]