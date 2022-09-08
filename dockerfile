from python:3.9-slim
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

LABEL maintainer="ahmed elnakeeb <ahmedelnakeeb2016@gmail.com>"

COPY /app/pip_requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app/
WORKDIR /app
CMD ["python3","main.py"]