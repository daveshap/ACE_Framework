#!/bin/bash

args=$*

docker build ./src/ace/app -t ace-base:latest ${args} -f ./src/ace/app/base.Dockerfile
