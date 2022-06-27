FROM python:3.7-slim 

LABEL author='cordy' version=1 broken_brains=100 

WORKDIR /app 

COPY ./requirements.txt ./ 

RUN pip3 install -r ./requirements.txt --no-cache-dir 

COPY ./ ./ 


ENV DB_NAME foodgram
ENV DB_PORT 5432 


CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]