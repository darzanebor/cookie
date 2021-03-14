FROM alpine:3.12 as base
COPY app/requirements.txt /usr/src/app/
RUN apk add --update --no-cache \
    python3 python3-dev \
    openssl bash \
    zlib curl && \
    apk add libxml2-dev libxslt-dev \
    libffi-dev gcc musl-dev libgcc \
    openssl-dev curl jpeg-dev zlib-dev \
    freetype-dev lcms2-dev openjpeg-dev \
    tiff-dev tk-dev tcl-dev && \
    curl https://bootstrap.pypa.io/get-pip.py -o- | python3 - && \
    python3 -m pip install pip && \
    pip3 install -r /usr/src/app/requirements.txt && \
    find / -type d -name __pycache__ -exec rm -r {} +   && \
    rm -rf /usr/lib/python*/ensurepip                   && \
    rm -rf /usr/lib/python*/turtledemo                  && \
    rm -rf /usr/lib/python*/idlelib                     && \
    rm -f /usr/lib/python*/turtle.py                    && \
    rm -f /usr/lib/python*/webbrowser.py                && \
    rm -f /usr/lib/python*/doctest.py                   && \
    rm -f /usr/lib/python*/pydoc.py                     && \
    rm -rf /root/.cache /var/cache
FROM base
ADD app /usr/src/app
RUN addgroup -S cookie && adduser -S cookie -G cookie && \
    chmod +x /usr/src/app/* && chown -R cookie:cookie /usr/src/app
EXPOSE 5000/tcp
USER cookie
WORKDIR /usr/src/app
ENTRYPOINT [ "/usr/src/app/entry.sh" ]
