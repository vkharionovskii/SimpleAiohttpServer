FROM gcc:11.3

COPY ./* /app/

RUN apt update && \
    apt install -y \
    python3-pip \
    && \
    pip install -r /app/requirements.txt \
    && \
    pytest /app/tests.py

ENTRYPOINT [ "python3", "/app/server.py", "--host", "127.0.0.1", "--port", "8080" ]
