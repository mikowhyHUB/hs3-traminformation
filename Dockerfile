ARG PYTHON_VERSION=3.11.2

FROM python:$PYTHON_VERSION-slim

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential=12.9 \
    curl=7.74.0-1.3+deb11u7 \
    gcc=4:10.2.1-1 \
    libxml2-dev=2.9.10+dfsg-6.7+deb11u3 \
    libxslt1-dev=1.1.34-4+deb11u1 \
    zlib1g-dev=1:1.2.11.dfsg-2+deb11u2 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser
USER appuser

WORKDIR /home/appuser/

ENV PYTHONPATH=/home/appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/*.py ./
CMD ["python", "main.py"]