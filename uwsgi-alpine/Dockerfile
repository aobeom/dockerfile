FROM alpine:3.7

ENV TMPDIR="/usr/local/src" \
    SOURCE="mirrors.ustc.edu.cn" \
    PYTHONTAR="Python-3.6.6" \
    PYTHONDIR="/usr/local/python"

COPY source/ $TMPDIR

RUN sed -i "s/dl-cdn.alpinelinux.org/$SOURCE/g" /etc/apk/repositories \
    && apk add --no-cache --virtual .build-deps \
           bzip2-dev \
           coreutils \
           dpkg-dev dpkg \
           expat-dev \
           findutils \
           gcc \
           gdbm-dev \
           libc-dev \
           libffi-dev \
           libnsl-dev \
           libressl \
           libressl-dev \
           libtirpc-dev \
           linux-headers \
           make \
           ncurses-dev \
           pax-utils \
           readline-dev \
           sqlite-dev \
           tcl-dev \
           tk \
           tk-dev \
           xz-dev \
           zlib-dev \
           musl-dev \
           libxslt-dev \
    && CORES=`cat /proc/cpuinfo | grep processor | wc -l` \
    && cd $TMPDIR \
    && tar xf ${PYTHONTAR}.tgz \
    && cd ${PYTHONTAR} \
    && ./configure --prefix=$PYTHONDIR \
    && make -j$CORES \
    && make install \
    && $PYTHONDIR/bin/pip3 --proxy 192.168.4.52:1080 install -r $TMPDIR/requirements.txt \
    # clean
    && runDeps=`scanelf --needed --nobanner --format '%n#p' --recursive /usr/local | tr ',' '\n' | sort -u | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }'` \
    && apk add --no-cache --virtual .rundeps $runDeps \
    && apk del .build-deps \
	&& rm -r $TMPDIR/*

ENTRYPOINT ["/usr/local/python/bin/uwsgi"]
CMD ["/bin/sh"]

EXPOSE 5000
