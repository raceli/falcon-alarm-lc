FROM ubuntu:14.04
MAINTAINER bwang@leancloud.rocks

ENV TERM xterm
WORKDIR /alarm
RUN echo "Asia/Shanghai" | sudo tee /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN adduser ubuntu
RUN apt-get update
RUN apt-get install -y curl python python-dev supervisor python-setuptools build-essential
RUN easy_install -U setuptools pip zc.buildout
RUN apt-get install -y nginx

RUN mkdir /alarm/src
ADD buildout.cfg setup.py /alarm/
RUN cd /alarm && buildout

ADD frontend /alarm/frontend
ADD src /alarm/src
ADD config /alarm/config

EXPOSE 80

CMD ["/usr/bin/supervisord","-n","-c","/alarm/config/supervisord.conf"]
