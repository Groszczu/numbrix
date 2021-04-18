FROM python:3.9.1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get install 

RUN apt-get update && apt-get install -y \
  libhdf5-serial-dev \
  netcdf-bin \
  libnetcdf-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt
COPY . /code/
