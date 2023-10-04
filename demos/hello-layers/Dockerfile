ARG BASE_IMAGE
FROM $BASE_IMAGE

WORKDIR /app

COPY src/ .

# TODO: Probably a cleaner way to do this.
RUN pip install -e .

COPY src/check_resource_health.py /usr/local/bin/check_resource_health.py
RUN chmod +x /usr/local/bin/check_resource_health.py
