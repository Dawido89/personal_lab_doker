# this is an official Python runtime, used as the parent image
# FROM docker.io/briantilburgs/aci-sdk:5.1.3e
FROM docker.io/briantilburgs/aci-sdk:5.2.8e-alpine2

#MAINTAINER Dawid Sandberg <dawidsandberg@gmail.com>

# Install & upgrade PIP and Setuptools
# prepared in image above
# RUN python3 -m pip install --upgrade pip && \
#    pip3 install setuptools

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
COPY . /app/

# execute everyone's favorite pip command, pip install -r
# RUN pip3 install -r requirements.txt

# execute the Flask app
CMD ["python3", "run.py"]
