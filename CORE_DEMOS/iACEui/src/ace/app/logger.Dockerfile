FROM python:3.11-slim

WORKDIR /ace/logger

COPY ./logger/requirements.txt /ace/logger
RUN pip install --no-cache-dir -r requirements.txt

COPY ./logger/app /ace/logger
COPY ./database /ace/logger/database

CMD ["python", "./app.py"]
