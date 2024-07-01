FROM python:3.11.4-slim-bullseye as prod
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*


RUN pip install poetry==1.8.3

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main

RUN apt-get update && \
    apt-get upgrade --assume-yes && \
    # cURL is necessary to invoke the "healthcheck" function using Docker
    apt-get install curl --assume-yes && \
    rm --recursive --force /var/lib/apt/lists/*

# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main

CMD ["/usr/local/bin/python", "-m", "backend"]

FROM prod as dev

RUN poetry install
