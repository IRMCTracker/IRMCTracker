FROM python:latest 

LABEL service="IRMCTracker" 

WORKDIR /irmctracker

COPY requirements.txt /irmctracker/

RUN bash && \
    apt-get update && \
    apt-get install git && \ 
    pip install -U pip && \ 
    pip install -r requirements.txt 

COPY . /irmctracker/ 

VOLUME /storage /storage

CMD ["python", "main.py"]