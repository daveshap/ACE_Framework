FROM ace-base:latest

WORKDIR /ace/app

COPY requirements.txt /ace/app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ /ace/app/

CMD ["python", "./controller.py"]