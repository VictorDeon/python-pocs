FROM python3:latest
WORKDIR /pocs
COPY ./pocs /pocs/
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
