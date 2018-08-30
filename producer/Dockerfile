FROM python:3.6.5
COPY /producer /producer/
COPY /general_helper/ /producer/general_helper/
WORKDIR /producer
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "client.py"]