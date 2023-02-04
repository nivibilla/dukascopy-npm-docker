# Use an official Python runtime as the base image
FROM python:3.8-slim

RUN mkdir dukascopy

# Set the working directory in the container
WORKDIR /dukascopy

# Copy the current directory contents into the container at /app
COPY . /dukascopy

# Install the required packages for Node.js and npm
RUN apt update
RUN apt install -y nodejs npm
RUN npm install dukascopy-node --save

# Install the dependencies listed in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./run.py"]