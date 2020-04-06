FROM python:3.6-alpine

RUN adduser -D statistics
WORKDIR /home/statistics
RUN python -m venv venv

#Install statistics api requirements
RUN venv/bin/pip install Flask
RUN venv/bin/pip install Flask-Caching
RUN venv/bin/pip install requests

# Install Web Server
RUN venv/bin/pip install gunicorn

copy app app
copy statistics.py boot.sh ./
RUN chmod a+x boot.sh
ENV FLASK_APP statistics.py

RUN chown -R statistics:statistics ./
USER statistics
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
