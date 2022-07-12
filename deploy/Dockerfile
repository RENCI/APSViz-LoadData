# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

##############
# Docker file for the creation of the stagedata script
#
# to create image: docker build -t load_geoserver:<version no> .
# to push image:
#       docker tag load_geoserver:<version no> renciorg/load_geoserver:<version no>
#       docker push renciorg/load_geoserver:<version no>
##############

FROM renciorg/gdal-python:gdal3.0.4-py3.8

# set the logging level
ENV LOG_LEVEL=10

# get some credit
LABEL maintainer="lisa@renci.org"

RUN apt-get update
RUN apt-get install -y libgnutls28-dev
RUN apt-get install -yq vim

# create a non-root user with a home directory
RUN useradd -m -d /home/nru -u 1000 nru

# switch to the new non-root user
USER nru

# make a directory for the repos and go there
RUN mkdir /home/nru/repo
WORKDIR /home/nru/repo

# get the repos
RUN git clone https://github.com/RENCI/APSViz-LoadData.git

# move to the install directory
WORKDIR /home/nru/repo/APSViz-LoadData
RUN git checkout develop

# install the pip requirements
RUN pip install -r requirements.txt

# create a directory for the ssh keys
RUN mkdir /home/nru/.ssh

# this dir was expected by the running pod. this will insure that it isnt defaulted to something else
RUN mkdir -p /home/nru/.config/matplotlib

# make everything read/write
RUN chmod 777 -R /home/nru

##########
# at this point the container is ready to accept the launch command.
##########
