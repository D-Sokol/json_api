FROM python:3.8

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

#RUN flask db upgrade
RUN python test.py

CMD flask db upgrade && gunicorn --access-logfile=logs/access.log --error-logfile=logs/errors.log --bind 0.0.0.0:8000 app:app
