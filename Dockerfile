FROM python:3.6

COPY . /usr/src/webchat/
RUN pip install --no-cache-dir -r /usr/src/webchat/requirements.txt

RUN chmod +x /usr/src/webchat/docker_run.sh

EXPOSE 5000 
EXPOSE 5678

CMD ["bash", "/usr/src/webchat/docker_run.sh"]
