FROM python:3.6-alpine

ENV APP=goobox-nodes-scraper
ENV WORKDIR=/srv/apps/$APP/app
ENV LOGDIR=/srv/apps/$APP/logs
ENV PYTHONPATH=$PYTHONPATH:$WORKDIR

# Install system dependencies
ENV RUNTIME_PACKAGES libxslt libxml2 jpeg tiff libpng zlib
ENV BUILD_PACKAGES build-base libxslt-dev libxml2-dev libffi-dev jpeg-dev tiff-dev libpng-dev zlib-dev openssl-dev
RUN apk --no-cache add $RUNTIME_PACKAGES

# Create initial dirs
RUN mkdir -p $WORKDIR $LOGDIR
WORKDIR $WORKDIR

# Install python requirements
COPY requirements.txt requirements_test.txt constraints.txt $WORKDIR/
RUN apk --no-cache add $BUILD_PACKAGES && \
    python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt -c constraints.txt && \
    python -m pip install --no-cache-dir -r requirements_test.txt -c constraints.txt && \
    apk del $BUILD_PACKAGES

# Copy application
COPY . $WORKDIR

ENTRYPOINT ["./run"]
