FROM debian:stretch-slim

ARG TMPDIR="/usr/local/src"
ARG PHPVER="7.2.8"
ARG PHPEXT_REDIS="4.1.0"
ARG PHPEXT_MONGO="1.5.1"
ARG USER="nginx"
ARG GROUP="nginx"

ARG PHPDIR="/usr/local/php"
ARG PHPETC=${PHPDIR}/etc
ARG PHPIZE=${PHPDIR}/bin/phpize
ARG PHPCONFIG=${PHPDIR}/bin/php-config

ARG http_proxy=""
ARG https_proxy=""

RUN >/etc/apt/sources.list \
    && echo "deb http://ftp.cn.debian.org/debian/ stretch main" > /etc/apt/sources.list \
    && echo "deb http://ftp.cn.debian.org/debian/ stretch-updates main" >> /etc/apt/sources.list \
    && echo "deb http://ftp.cn.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
                        gcc \
                        libxml2-dev \
                        libssl-dev \
                        libbz2-dev \
                        libcurl4-gnutls-dev \
                        libpng-dev \
                        make \
                        autoconf \
                        curl \
    && useradd -c "Web Server" -U nginx -M -s /usr/sbin/nologin \
    # php main
    && CORES=`cat /proc/cpuinfo | grep processor | wc -l` \
    && cd $TMPDIR \
    && ln -s /usr/include/x86_64-linux-gnu/curl /usr/local/include/curl \
    && ln -s /usr/lib/x86_64-linux-gnu/libssl.so /usr/lib/libssl.so \
    && curl -O http://pecl.php.net/get/mongodb-${PHPEXT_MONGO}.tgz \
    && curl -O http://pecl.php.net/get/redis-${PHPEXT_REDIS}.tgz \
    && curl -O http://jp2.php.net/distributions/php-${PHPVER}.tar.gz \
    && tar xf php-${PHPVER}.tar.gz \
    && cd php-${PHPVER} \
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
    # php-ext
    && cd $TMPDIR/php-${PHPVER}/ext/mysqli \
    && $PHPIZE && ./configure --with-php-config=$PHPCONFIG --with-mysqli=mysqlnd \
    && make -j$CORES && make install \
    && cd $TMPDIR && tar xf redis-${PHPEXT_REDIS}.tgz && tar xf mongodb-${PHPEXT_MONGO}.tgz \
    && cd $TMPDIR/redis-${PHPEXT_REDIS} \
    && $PHPIZE && ./configure --with-php-config=$PHPCONFIG \
    && make -j$CORES && make install \
    && cd $TMPDIR/mongodb-${PHPEXT_MONGO} \
    && $PHPIZE && ./configure --with-php-config=$PHPCONFIG \
    && make -j$CORES && make install \
    # clean
    && rm -r /var/lib/apt/lists/* \
    && rm -fr $TMPDIR/* \
    && apt-get clean \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

EXPOSE 9000
CMD ["/usr/local/php/sbin/php-fpm"]

