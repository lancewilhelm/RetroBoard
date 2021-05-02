FROM python:3.7-slim-buster

WORKDIR /app
ADD . .
RUN pip3 install -r requirements.txt
RUN sh rgb_matrix_setup.sh
EXPOSE 5000
CMD [ "sudo", "python3", "main.py" ]