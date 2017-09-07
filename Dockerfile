FROM python:3.6

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY app.py /usr/src/app/
COPY index.html /usr/src/app/
COPY server.py /usr/src/app/
COPY run.sh /usr/src/app/
RUN chmod +x /usr/src/app/run.sh

EXPOSE 5000 
EXPOSE 5678

CMD ["bash", "/usr/src/app/run.sh"]
