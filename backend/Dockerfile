FROM python:3.8-alpine

ENV FLASK_APP /backend/app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

COPY ./requirements.txt ./backend/
    
RUN apk add --no-cache bash && \
    pip3 install -r ./backend/requirements.txt

COPY . ./backend

ENTRYPOINT ["/backend/entrypoint.sh"]
