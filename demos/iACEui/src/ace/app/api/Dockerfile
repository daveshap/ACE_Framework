FROM ace-base:latest

WORKDIR /ace/app

COPY requirements.txt /ace/app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ /ace/app/

# This needs to be removed and tested.  We don't want to include the .env file in the images.
# COPY ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
