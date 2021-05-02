FROM python:3.7

WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "./main.py" ]