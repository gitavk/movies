FROM python:3.11-slim

COPY ./requirements ./requirements
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r ./requirements/dev.txt

WORKDIR app/
COPY src/ src/
COPY tests/ tests/

RUN useradd -ms /bin/bash appuser
RUN chown appuser -R /app
USER appuser

CMD ["pytest", "--cov-report=term-missing", "--cov=src", "-p", "no:cacheprovider", "./tests"]
