FROM python:3.10.12-slim-bookworm
    
# RUN echo 'deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main' >> /etc/apt/sources.list \
#     && apt-get update \
#     && apt-get install -y --no-install-recommends apt-utils

RUN apt-get update \
    && apt-get -y dist-upgrade \
    && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y netcat-openbsd && apt-get autoremove -y

# Create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
# COPY ./sparql_templates /code/sparql_templates
# COPY ./config_streamgraphiti.cfg /code/config_streamgraphiti.cfg

COPY ./run.sh /code/run.sh
COPY ./wait_for_services.sh /code/wait_for_services.sh

WORKDIR /code

# ENTRYPOINT ["./wait_for_services.sh"] 
CMD ["./run.sh", "${WORKER}", "${WORKER_PORT}", "${CONFIG_CLASS}"]

# CMD ["faust -A app.main worker -l info"]