FROM python:3.6.5
ADD . /producer
WORKDIR /producer
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "client.py"]