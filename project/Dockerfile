FROM python:3.6

ADD . /app       
WORKDIR /app     

RUN pip install --upgrade pip           
RUN pip install -r requirements.txt    
RUN apt-get update ##[edited]
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y 

EXPOSE 5000    
CMD ["python","run.py"]

