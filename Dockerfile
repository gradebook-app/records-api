FROM python:3.13-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/app

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
