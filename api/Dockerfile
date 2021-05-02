FROM python:3.7-alpine

WORKDIR /app
ADD . /app
RUN sudo pip3 install -r requirements.txt
CMD [ "sudo", "./main.py" ]