FROM node:13.12.0-alpine


COPY ./package.json ./frontend/
COPY ./package-lock.json ./frontend/
RUN npm --prefix ./frontend install --verbose && \
    apk add --no-cache bash

COPY . ./frontend

ENTRYPOINT ["/frontend/entrypoint.sh"]
