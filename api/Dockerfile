FROM python:3.7-buster

WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
RUN sh rgb_matrix_setup.sh
EXPOSE 5000
CMD [ "python3", "main.py" ]