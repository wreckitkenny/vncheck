FROM python:3.8-slim
RUN apt update && apt install git -y
RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt