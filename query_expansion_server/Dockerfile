FROM python:3.8-slim
COPY app /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
	git \
	openjdk-17-jdk \
	openjdk-17-jre \
	postgresql-client 

RUN pip install --upgrade pip
RUN pip install flask sqlalchemy psycopg2-binary
RUN pip install --upgrade git+https://github.com/terrier-org/pyterrier.git#egg=python-terrier 
