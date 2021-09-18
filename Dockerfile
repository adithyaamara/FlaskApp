FROM python:3.7-slim-buster
RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py /app/main.py
COPY templates/ app/templates
COPY /static/ /app/static
EXPOSE 4444
CMD [ "python3", "-u", "./main.py" ]
