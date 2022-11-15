FROM python:3.9-slim

RUN useradd --user-group -r app

WORKDIR /home/app

COPY . .

RUN chown -R app:app /home/app

USER app

RUN pip3 install -r requirements.txt --no-warn-script-location

ENTRYPOINT [ "python", "main.py" ]