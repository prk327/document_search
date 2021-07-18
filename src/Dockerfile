# first stage
FROM python:3.8 AS builder
COPY ./src/requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# second unnamed stage
FROM python:3.8-slim
WORKDIR /code

RUN apt-get -q update && apt-get -qy install netcat curl \
    && rm -rf /var/lib/apt/lists/*

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./src .

# update PATH environment variable
ENV PATH=/root/.local:$PATH

EXPOSE 5000

CMD [ "python", "./service.py" ]