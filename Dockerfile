FROM python:3.6-alpine

RUN adduser -D statistics
WORKDIR /home/statistics
RUN python -m venv venv
RUN apk add sqlite
RUN apk add gcc
RUN apk add g++
RUN apk add make

RUN chown -R statistics:statistics ./
#Install statistics api requirements
RUN venv/bin/pip install Flask
RUN venv/bin/pip install Flask-Caching
RUN venv/bin/pip install requests
RUN venv/bin/pip install flask-cors
RUN venv/bin/pip install pandas

# Install Web Server
RUN venv/bin/pip install gunicorn
RUN venv/bin/pip install SQLAlchemy

copy app app
copy statistics.py boot.sh ./
RUN chmod a+x boot.sh
ENV FLASK_APP statistics.py

USER statistics
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
