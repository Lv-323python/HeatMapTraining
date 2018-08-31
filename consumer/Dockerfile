FROM python:3.6.5
COPY /consumer /consumer/
COPY /general_helper/ /consumer/general_helper/
WORKDIR /consumer
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "receiver.py"]
