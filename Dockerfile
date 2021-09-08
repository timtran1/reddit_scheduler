FROM python:3.9-alpine

COPY . /usr/app
WORKDIR /usr/app

RUN pip install -r requirements.txt

COPY cron.crontab /etc/cron.d/reddit_scheduler
RUN chmod 0644 /etc/cron.d/reddit_scheduler
RUN crontab /etc/cron.d/reddit_scheduler
RUN touch /var/log/cron.log

ENTRYPOINT ["sh", "entrypoint.sh"]