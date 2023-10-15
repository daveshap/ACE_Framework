FROM ace-base:latest

WORKDIR /ace/app

COPY ./api/requirements.txt /ace/app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api/app/ /ace/app
COPY ./database /ace/app/database

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
