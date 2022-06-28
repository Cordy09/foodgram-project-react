FROM python:3.7-slim 

LABEL author='cordy' version=1 broken_brains=100 

WORKDIR /app 

COPY ./requirements.txt ./ 

RUN pip3 install -r ./requirements.txt --no-cache-dir 

COPY ./ ./ 

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]