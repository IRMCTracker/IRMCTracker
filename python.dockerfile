FROM python:3.9-slim

RUN useradd --user-group -r app

COPY --chown=app:app requirements.txt /app/

USER app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project
COPY --chown=app:app . /app

ENTRYPOINT [ "python", "main.py", "run"]
