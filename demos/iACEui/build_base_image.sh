#!/bin/bash

args=$*

docker build ./src/ace/app/base -t ace-base:latest ${args}