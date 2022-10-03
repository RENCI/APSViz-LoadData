# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

##############
# Docker file for the creation of the APSVix-LoadData image.
# stage 1: create a conda virtual environment
##############
FROM continuumio/miniconda3 as build

# get some credit
LABEL maintainer="lisa@renci.org"

# extra metadata
LABEL version="v0.0.1"
LABEL description="APSVis LoadData - Loads data into a geoserver."

# update conda
RUN conda update conda

# Needed for pycurl
ENV PYCURL_SSL_LIBRARY=openssl

# Create the virtual environment
COPY environment.yml .
RUN conda env create -f environment.yml

# install conda pack to compress this stage
RUN conda install -c conda-forge conda-pack

# conpress the virtual environment
RUN conda-pack -n load_data -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# fix up the paths
RUN /venv/bin/conda-unpack

##############
# stage 2: create a python implementation using the stage 1 virtual environment
##############
FROM python:3.9-slim

RUN apt-get update

# install wget and bc
RUN apt-get install -y wget git

# clear out the apt cache
RUN apt-get clean

# add user nru and switch to it
RUN useradd --create-home -u 1000 nru
USER nru

# move the the code location
WORKDIR /home/nru/load_data

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

# declare the virtual environment location
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

# Copy in the rest of the code
COPY common common
COPY styles styles
COPY geo geo
COPY ./*.py ./

# set the python path
ENV PYTHONPATH=/home/nru/load_data

# set the log dir. use this for debugging if desired
ENV LOG_PATH=/data/logs

##########
# at this point the container is ready to accept the launch command.
# ex: python load-geoserver-images.py --instanceId lisa_4164-2022072906-namforecast
##########

