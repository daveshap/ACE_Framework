#!/usr/bin/env bash

docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up "$@"
