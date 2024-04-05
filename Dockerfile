FROM python:3.10
WORKDIR /software
COPY . /software/
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
EXPOSE 8000
CMD uvicorn main:app --workers 1 --host 0.0.0.0 --port 8000
