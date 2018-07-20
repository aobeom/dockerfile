FROM alpine:3.7

# global
ENV TMPDIR="/usr/local/src" \
    SOURCE="mirrors.ustc.edu.cn" \
    PHPTAR="php-7.2.5" \
    PHPEXT_REDIS="phpredis-3.1.6" \
    PHPEXT_MONGO="mongodb-1.4.2" \
    # configure
    USER="nginx" GROUP="nginx"

ENV PHPDIR="/usr/local/php"
ENV PHPETC=${PHPDIR}/etc \
    PHPIZE=${PHPDIR}/bin/phpize \
    PHPCONFIG=${PHPDIR}/bin/php-config \
    PHPFPM=${PHPDIR}/sbin/php-fpm

COPY source/ $TMPDIR

RUN sed -i "s/dl-cdn.alpinelinux.org/$SOURCE/g" /etc/apk/repositories \
    && apk add --no-cache --virtual .build-deps \
                          gcc \
                          g++ \
                          bzip2-dev \
                          openssl-dev \
                          libxml2-dev \
                          gd-dev \
                          libpng-dev \
                          gettext-dev \
                          make \
                          curl-dev \
                          autoconf \
    && addgroup $GROUP \
    && adduser -D -H -G $GROUP $USER \
    # php main
    && CORES=`cat /proc/cpuinfo | grep processor | wc -l` \
    && cd $TMPDIR \
    && tar xf ${PHPTAR}.tar.gz \
    && cd $TMPDIR/$PHPTAR \
    && ./configure --prefix=$PHPDIR \
                   --sysconfdir=$PHPETC \
                   --with-config-file-path=$PHPETC \
                   --with-openssl \
                   --with-zlib \
                   --with-bz2 \
                   --with-curl \
                   --with-libxml-dir \
                   --with-gd \
                   --enable-mbstring \
                   --enable-fpm \
                   --with-fpm-user=$USER \
                   --with-fpm-group=$GROUP \
                   --enable-sockets \
                   --enable-bcmath \
                   --with-gettext \
                   --enable-mysqlnd \
                   --with-pdo-mysql \
                   --enable-opcache \
                   --enable-xml \
                   --enable-pdo \
    && make -j$CORES \
    && make install \
    && cp $TMPDIR/$PHPTAR/php.ini-production $PHPETC/php.ini \
    && cp $TMPDIR/php-fpm.conf $PHPETC \
    && cp $TMPDIR/www.conf $PHPETC/php-fpm.d/ \
    # php-ext
    && cd $TMPDIR/$PHPTAR/ext/mysqli \
    && $PHPIZE && ./configure --with-php-config=$PHPCONFIG --with-mysqli=mysqlnd \
    && make -j$CORES && make install \
    && cd $TMPDIR && tar xf ${PHPEXT_REDIS}.tar.gz && tar xf ${PHPEXT_MONGO}.tgz \
    && cd $TMPDIR/$PHPEXT_REDIS \
    && $PHPIZE && ./configure --with-php-config=$PHPCONFIG \
    && make -j$CORES && make install \
    && cd $TMPDIR/$PHPEXT_MONGO \
    && $PHPIZE && ./configure --with-php-config=$PHPCONFIG \
    && make -j$CORES && make install \
    && echo "expose_php=Off" >> $PHPETC/php.ini \
    && echo "extension=mysqli.so" >> $PHPETC/php.ini \
    && echo "extension=redis.so" >> $PHPETC/php.ini \
    && echo "extension=mongodb.so" >> $PHPETC/php.ini \
    # clean
    && runDeps=`scanelf --needed --nobanner --format '%n#p' --recursive /usr/local | tr ',' '\n' | sort -u | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }'` \
    && apk add --no-cache --virtual .rundeps $runDeps \
    && apk del .build-deps \
    && rm -fr $TMPDIR/*

EXPOSE 9000
CMD ["/usr/local/php/sbin/php-fpm"]
