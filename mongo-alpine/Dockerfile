FROM alpine:3.7

RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g" /etc/apk/repositories \
    && apk add --no-cache --virtual .build-deps \
           mongodb

CMD ["mongod","--config","/usr/local/mongodb/confs/mongod.conf"]
