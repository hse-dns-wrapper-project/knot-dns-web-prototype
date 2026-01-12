FROM python:3.12

WORKDIR /app

# Set Python libs
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

# Setup entrypoint
COPY ./docker/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/knot-dns-web/entrypoint.sh"]