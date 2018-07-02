FROM python:3.6.5
LABEL maintainer="Khalid Peer <khalid.peer233@gmail.com>"

WORKDIR /home

# copy requirements first to cache the deps
COPY requirements.txt /home
RUN pip3 install -r requirements.txt

# copy the rest of the source
COPY / /home

ENTRYPOINT ["python3", "sampler.py"]
