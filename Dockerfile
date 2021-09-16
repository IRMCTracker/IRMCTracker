FROM python:latest 

LABEL service="IRMCTracker" 

WORKDIR /irmctracker

COPY requirments.txt /irmctracker/

RUN bash && \
    apt-get update && \
    apt-get install git && \ 
    pip install -U pip && \ 
    pip install -r requirments.txt

COPY . /irmctracker/ 

VOLUME /storage /storage

CMD ["python", "main.py"]