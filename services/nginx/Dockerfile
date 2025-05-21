FROM nginx:1.27.5-alpine

ARG DOMAIN_NAME
ENV DOMAIN_NAME=${DOMAIN_NAME}

RUN apk add openssl && \
    mkdir -p /etc/nginx/ssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/hypertube.key \
        -out /etc/nginx/ssl/hypertube.crt \
        -subj "/C=FR/ST=GES/L=Mulhouse/O=42/OU=42/CN=${DOMAIN_NAME}"

        
COPY ./default.conf /etc/nginx/conf.d/default.conf

RUN sed -i "s|localhost|${DOMAIN_NAME}|g" /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
