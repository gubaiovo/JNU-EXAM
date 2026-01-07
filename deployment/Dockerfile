FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y git nginx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY generate_json.py /app/generate_json.py

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]