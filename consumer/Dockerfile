FROM python:3.6.5
RUN mkdir top
ADD . top/consumer
WORKDIR top/consumer
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /top
ENV PYTHONPATH="$PYTHONPATH:/top"
CMD python consumer/receiver.py