FROM python:3.7-alpine

WORKDIR /app
ADD . /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD [ "./main.py" ]