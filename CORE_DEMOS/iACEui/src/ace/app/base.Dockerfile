# FROM python:3.11-slim

# WORKDIR /ace/app/base

# COPY requirements.txt /ace/app/base
# RUN pip install --no-cache-dir -r requirements.txt

# COPY ./base_layer.py /ace/app/base
# COPY ./settings.py /ace/app/base
# COPY ./prompts.py /ace/app/base
# COPY ./amqp/ /ace/app/base/amqp
# COPY ../database/ /ace/app/base/database


FROM python:3.11-slim

WORKDIR /ace/app/base

COPY base.requirements.txt /ace/app/base/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./base /ace/app/base
COPY ./database/ /ace/app/database

