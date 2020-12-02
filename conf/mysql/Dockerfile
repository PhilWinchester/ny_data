FROM mysql:5.7.16

ADD init.sql /

# overrides CMD from mysql image to use init file
# https://github.com/docker-library/mysql/blob/eeb0c33dfcad3db46a0dfb24c352d2a1601c7667/5.7/Dockerfile#L75
# CAUTION: init file does not support sql comments
CMD ["mysqld", "--init-file=/init.sql"]
