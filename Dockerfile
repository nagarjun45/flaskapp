FROM python:2.7-alpine3.7
RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
LABEL maintainer="Nagarjun" \
      Version="1.0"
CMD flask run --host=0.0.0.0 --port=5000
    