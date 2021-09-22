FROM python:latest 

LABEL service="IRMCTracker" 

WORKDIR /irmctracker

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN bash && \
    apt-get update && \
    apt-get install git && \ 
    pip install -U pip && \ 
    pip install -r requirments.txt

COPY . /irmctracker/ 

VOLUME /storage /storage

CMD ["python", "main.py"]