FROM python:3.8-slim
RUN sed -i 's/http:\/\/deb.debian.org/https:\/\/artifact.vnpay.vn\/nexus\/repository\/apt-proxy_deb.debian.org/g' /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN apt update && apt install git -y
RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN cp /app/pip.conf /etc/pip.conf
RUN pip install -r requirements.txt