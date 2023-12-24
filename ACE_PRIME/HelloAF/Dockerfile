ARG BASE_IMAGE
FROM $BASE_IMAGE

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev
RUN apt-get update && apt-get install -y --no-install-recommends curl net-tools
RUN apt-get update && apt-get install -y --no-install-recommends vim procps less
RUN apt-get update && apt-get install -y --no-install-recommends figlet toilet cowsay

COPY src/ .

# TODO: Probably a cleaner way to do this.
RUN pip install -e .

COPY src/check_resource_health.py /usr/local/bin/check_resource_health.py
RUN chmod +x /usr/local/bin/check_resource_health.py
