FROM python:3.6.5
ADD . /consumer
WORKDIR /consumer
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "receiver.py"]