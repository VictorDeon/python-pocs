FROM python:3.10
WORKDIR /pocs
COPY ./pocs /pocs/
COPY requirements.txt /tmp/requirements.txt
COPY health_check.py /tmp/health_check.py
RUN pip install -r /tmp/requirements.txt
CMD [ "python3", "/tmp/health_check.py" ]