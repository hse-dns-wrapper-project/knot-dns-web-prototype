FROM cznic/knot:latest

WORKDIR /app

COPY requirements.txt requirements.txt

RUN \
    apt-get update && \
    apt-get install python3 -y && \
    apt-get install python3-pip -y && \
    apt-get install python3-venv -y && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m venv /.venv && \
    . /.venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

# Setup entrypoint
COPY ./docker/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]