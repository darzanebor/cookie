FROM alphaceti/default-python:0.1.3 as base
ENV PROMETHEUS_MULTIPROC_DIR="/usr/src/app/prometheus" \
    PATH="${PATH}:/home/cookie/.local/bin"
ADD app /usr/src/app
RUN addgroup -S cookie && \
    adduser -S cookie -G cookie && \
    chmod +x /usr/src/app/* && \
    chown -R cookie:cookie /usr/src/app && \
    apk add --update --no-cache \
    python3-dev \
    openssl-dev \
    libxml2-dev \
    libxslt-dev \
    freetype-dev \
    openjpeg-dev \
    libffi-dev \
    lcms2-dev \
    tiff-dev \
    jpeg-dev \
    zlib-dev \
    musl-dev \
    tcl-dev \
    tk-dev \
    openssl \    
    zlib \
    curl \
    g++ \
    libgcc \
    libmagic
EXPOSE 5000/tcp
USER cookie
WORKDIR /usr/src/app
RUN pip3 install --no-cache-dir -r ./requirements.txt
ENTRYPOINT [ "./entry.sh" ]
