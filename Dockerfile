from python:3.12.0b3-alpine3.18
WORKDIR /app
COPY . /app


RUN pip install -r requirements1.txt
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]