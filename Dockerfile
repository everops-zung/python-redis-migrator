FROM python:3
# FROM finalduty/archlinux:daily
#MAINTAINER jeremy@checkr.com

#RUN pacman -Sy --noconfirm python
#RUN pacman -Sy --noconfirm python2 python2-click python2-progressbar python2-redis tmux
RUN pip3 install click progressbar redis

ADD migrate-redis.py /migrate-redis.py
