FROM python:3.7-buster

WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
RUN sh rgb_matrix_setup.sh
RUN export PATH=$PATH:/bin
EXPOSE 5000
CMD [ "sudo", "python3", "main.py" ]