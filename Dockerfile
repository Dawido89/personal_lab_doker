FROM python:3.7-slim

LABEL Dawid Sandberg <dawidsandberg@gmail.com>

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
COPY . /app/

# execute everyone's favorite pip command, pip install -r
RUN pip3 install --upgrade setuptools pip
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

# execute the script 
CMD ["python3", "./config_fetch_OOB2.py"]

