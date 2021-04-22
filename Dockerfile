FROM python:3.7.10-buster
WORKDIR /app
RUN pip install boto3 moto pytest pytest-mock pyyaml