ARG ARCH=
FROM ${ARCH}ubuntu:focal
MAINTAINER info@cstan.io

# Install mplayer, alsa and Python stuff
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y mplayer alsa-base alsa-tools python3-pip python3-flask sqlite3 psmisc && apt-get clean

# create application directory
RUN mkdir -p /opt/radio_api/radio_api
ADD radio_api /opt/radio_api/radio_api
ADD entrypoint.sh /opt/radio_api/entrypoint.sh

# volume configuration
VOLUME ["/opt/radio_api/instance"]

# start application
CMD "/opt/radio_api/entrypoint.sh"

# listen on port 5000
EXPOSE 5000
