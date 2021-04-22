FROM python:3.7.10-buster
RUN pip install boto3 moto pytest pytest-mock pyyaml