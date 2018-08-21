FROM python:3.6.5
ADD /consumer /consumer/
ADD /general_helper/ /consumer/general_helper/
WORKDIR /consumer
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "receiver.py"]
