FROM python:3.6.5-alpine3.7

# Update the apt-get list
RUN apt-get update -y

# Install python dependencies
RUN apt-get install -y python-pip python-dev build-essential

# Install curl for installing nodejs
RUN apt-get install -y curl

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .