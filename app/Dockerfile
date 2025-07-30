# Use official Python image as base
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip
RUN pip install -r requirements.txt

COPY . .