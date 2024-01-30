FROM python:3.11-slim


RUN apt-get -y update &&  \ 
    apt-get install --no-install-recommends  \
    -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements ./requirements
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r ./requirements/prod.txt

WORKDIR app/
COPY src/ src/
EXPOSE 8000
RUN useradd -ms /bin/bash appuser
RUN chown appuser -R /app
USER appuser

COPY docker-files/start.sh ids.txt ./
CMD ["./start.sh"]
