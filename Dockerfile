FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt update && pip install poetry