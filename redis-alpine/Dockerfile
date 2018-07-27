FROM alpine:3.7

ARG TMPDIR="/usr/local/src"
ARG SOURCE="mirrors.ustc.edu.cn"
ARG GROUP="redis"
ARG USER="redis"
ARG REDISVER="4.0.10"
ARG REDISDAT="/data/redis"
ARG REDISDIR="/usr/local/redis"

RUN sed -i "s/dl-cdn.alpinelinux.org/$SOURCE/g" /etc/apk/repositories \
    && apk add --no-cache --virtual .build-deps \
           curl \
           coreutils \
           gcc \
           jemalloc-dev \
           linux-headers \
           make \
           musl-dev \
    && addgroup $GROUP \
    && adduser -D -H -G $GROUP $USER \
    && mkdir -p $TMPDIR \
    && cd $TMPDIR \
    && CORES=`cat /proc/cpuinfo | grep processor | wc -l` \
    && curl -O http://download.redis.io/releases/redis-${REDISVER}.tar.gz \
    && tar xf redis-${REDISVER}.tar.gz \
    && REDISSRC=$TMPDIR/redis-${REDISVER}/src \
	&& grep -q '^#define CONFIG_DEFAULT_PROTECTED_MODE 1$' $REDISSRC/server.h \
	&& sed -ri 's!^(#define CONFIG_DEFAULT_PROTECTED_MODE) 1$!\1 0!' $REDISSRC/server.h \
	&& grep -q '^#define CONFIG_DEFAULT_PROTECTED_MODE 0$' $REDISSRC/server.h \
    && cd $REDISSRC \
    && make -j$CORES \
    && make install \
    && mkdir -p $REDISDAT \
    && chown $USER:$GROUP $REDISDAT \
    # clean
    && runDeps=`scanelf --needed --nobanner --format '%n#p' --recursive /usr/local | tr ',' '\n' | sort -u | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }'` \
    && apk add --no-cache --virtual .rundeps $runDeps \
    && apk del .build-deps \
	&& rm -r $TMPDIR/*

VOLUME $REDISDAT
WORKDIR $REDISDAT
CMD ["redis-server", "/usr/local/redis/redis.conf"]

EXPOSE 6379

