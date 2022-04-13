FROM python:3.10-bullseye
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade pip
COPY ./requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
COPY . .