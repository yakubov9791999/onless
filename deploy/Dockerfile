FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y netcat vim cron
RUN touch /var/log/cron.log
#RUN adduser yakubov
#USER yakubov
WORKDIR /code

#COPY --chown=yakubov:yakubov requirements.txt requirements.txt
COPY deploy/requirements.txt requirements.txt
COPY deploy/crontab /etc/cron.d/crontab

#ENV PATH="/home/yakubov/.local/bin:/usr/local/bin:${PATH}"

RUN pip install --upgrade pip && pip install -r requirements.txt

#COPY --chown=yakubov:yakubov / /
COPY . /code
COPY deploy/entrypoint.sh /
RUN chmod +x /entrypoint.sh
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab deploy/crontab
RUN chmod +x /code/deploy/cron_script.sh
CMD ["cron", "-f"]
CMD /etc/init.d/cron start
ENTRYPOINT ["sh", "/entrypoint.sh"]

#RUN mkdir /code
#WORKDIR /code
#COPY requirements.txt /code/
#RUN pip install -r requirements.txt
## copy entrypoint.sh
##COPY . /code/
#CMD bash /code/deploy/entrypoint.sh
