FROM ubuntu:18.04

COPY . /usr/src/chat

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN pip3 install --no-cache-dir -r /usr/src/chat/RESTful_server/requirements.txt

EXPOSE 5000 

CMD ["/usr/bin/python3", "/usr/src/chat/RESTful_server/main.py"]
