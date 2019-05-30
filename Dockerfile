FROM python:alpine

ADD app ./app
ADD smarthome_website.py .
ADD requirements.txt .

WORKDIR .

RUN pip3 install -r requirements.txt

CMD ["python3", "smarthome_website.py"]
