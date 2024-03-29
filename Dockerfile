FROM python:3.8
RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py /app/main.py
COPY .env /app/.env
COPY templates/ /app/templates
COPY /static/ /app/static
COPY /addons/ /app/addons/
COPY /admin/ /app/admin/
COPY /guest/ /app/guest/
EXPOSE 4444
CMD [ "python3", "./main.py" ]
