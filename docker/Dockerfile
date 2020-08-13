FROM mysql:5.7.12

MAINTAINER charsyam <charsyam@naver.com>

ENV MYSQL_ROOT_PASSWORD redismon!@#
ENV MYSQL_USER redismon
ENV MYSQL_PASSWORD redismon!@#
ENV MYSQL_DATABASE redismon

COPY etc/ /etc/mysql/conf.d/
RUN cat /usr/share/zoneinfo/Asia/Seoul > /etc/localtime
