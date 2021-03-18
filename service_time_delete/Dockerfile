FROM python:3.6

ADD . /time_delete       
WORKDIR /time_delete     

RUN pip install --upgrade pip           
RUN pip install -r requirements.txt    
RUN apt-get update ##[edited]
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y 

EXPOSE 4005     
CMD ["python","run.py"]

