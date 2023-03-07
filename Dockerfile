FROM python:3.10
COPY . .
RUN apt-get update 
RUN apt-get -y install ffmpeg
RUN apt-get -y install libffi-dev
RUN apt-get -y install libnacl-dev 
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
 

