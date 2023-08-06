FROM balenalib/armv7hf-alpine:3.9

RUN [ "cross-build-start" ]
RUN apk --update add python3 bash perl curl wget grep sed docker sudo mysql-client postgresql-client make git supervisor tzdata \
                     sshpass openssh-client
RUN [ "cross-build-end" ]

ADD . /infracheck
ADD .git /infracheck/

ENV CHECK_INTERVAL="*/1 * * * *" \
    WAIT_TIME=0\
    LAZY=false

RUN [ "cross-build-start" ]
RUN cd /infracheck \
    # install as a package
    && git remote remove origin || true \
    && git remote add origin https://github.com/riotkit-org/infracheck.git \
    && apk add --update gcc python3-dev musl-dev linux-headers postgresql-dev \
    && make install \
    # after installing as package extract infrastructural files
    \
    && cp -pr /infracheck/entrypoint.sh / \
    && cp -pr /infracheck/supervisord.conf /etc/supervisord.conf \
    && chmod +x /entrypoint.sh \
    \
    # delete the temporary directory after the application was installed via setuptools
    && rm -rf /infracheck \
    \
    # simple check that application does not crash at the beginning (is correctly packaged)
    && infracheck --help \
    \
    && apk del gcc python3-dev musl-dev linux-headers postgresql-dev
RUN [ "cross-build-end" ]

ENTRYPOINT ["/entrypoint.sh"]
