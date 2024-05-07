FROM python:3.11

# Environment variables ensure Python outputs all in terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# Add the rest of the code
COPY . /usr/src/app/

