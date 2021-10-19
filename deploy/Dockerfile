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

# make a directory for the repos and go there
RUN mkdir /repo
WORKDIR /repo

# get the repos
RUN git clone https://github.com/RENCI/APSViz-LoadData.git

# move to the install directory
WORKDIR /repo/APSViz-LoadData

RUN apt-get install -y libgnutls28-dev
# install the pip requirements
RUN pip install -r requirements.txt

##########
# at this point the container is ready to accept the launch command.
##########
