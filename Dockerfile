FROM python:3.11-alpine
WORKDIR /app
ADD /flask-server /app/flask-server
COPY requirements.txt /app/flask-server
RUN mkdir -p /app/flask-server/venv
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV VIRTUAL_ENV=/app/flask-server/venv
RUN python3 -m venv $VIRTUAL_ENV
WORKDIR /app/flask-server
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install --upgrade pip
# Install grpcio (gcc, g++, linux-headers) psycopg2 (musl-dev postgresql-libs postgresql-dev) dependencies
RUN apk update && \ 
    # postgresql-libs must be installed on the system for psycopg2 
    apk add --no-cache postgresql-libs && \
    # all of these dependencies are only needed during build time for grpcio & psychopg2, hence the --virtual flag and --purge
    apk add --no-cache --virtual .build-deps postgresql-dev gcc g++ linux-headers musl-dev && \
    pip3 install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# Run the web service on container startup. Here we use the gunicorn
# webserver, with 3 worker processes and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
WORKDIR /app
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --threads 8 --timeout 0 --chdir flask-server main:app

# [END run_python_service]

