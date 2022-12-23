# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=1

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip3 install --no-cache-dir -r requirements.txt

ENV NEW_RELIC_APP_NAME=petrosa-crypto-candles-consistency-checker
ENV NEW_RELIC_CONFIG_FILE=newrelic.ini

RUN sh deploy/buildconfig.sh

ENTRYPOINT ["newrelic-admin", "run-program", "python", "main.py"]
