ARG BASE_IMAGE
FROM $BASE_IMAGE

WORKDIR /app

COPY src/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY src/ .

COPY src/check_resource_health.py /usr/local/bin/check_resource_health.py
RUN chmod +x /usr/local/bin/check_resource_health.py
