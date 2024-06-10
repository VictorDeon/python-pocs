FROM python:3.10
WORKDIR /software
COPY . /software/
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libcairo2-dev \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libgdk-pixbuf2.0-dev \
    shared-mime-info \
    fonts-liberation \
    && apt-get clean
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
EXPOSE 8000
CMD uvicorn main:app --workers 1 --host 0.0.0.0 --port 8000
