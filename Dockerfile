ARG BASE_IMAGE_TAG

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BUILD ETL BASE PROCESSOR
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM python:$BASE_IMAGE_TAG as base_processor

ARG APK_PACKAGES
ARG PIP_PACKAGES

RUN apk add --no-cache $APK_PACKAGES && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir $PIP_PACKAGES

COPY base_processor /usr/local/lib/python2.7/site-packages/base_processor
COPY bashlog        /bin/bashlog

ENTRYPOINT [""]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BUILD ETL BASE PROCESSOR TEST
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM python:$BASE_IMAGE_TAG as base_processor_test

ARG APK_PACKAGES
ARG APK_TEST_PACKAGES
ARG PIP_PACKAGES
ARG PIP_TEST_PACKAGES

RUN apk -v --update add --no-cache ${APK_PACKAGES} ${APK_TEST_PACKAGES} && \
    pip install --upgrade --no-cache-dir pip && \
    pip install --upgrade --no-cache-dir ${PIP_PACKAGES} ${PIP_TEST_PACKAGES}

COPY base_processor /usr/local/lib/python2.7/site-packages/base_processor
COPY bashlog        /bin/bashlog

ENTRYPOINT [""]
