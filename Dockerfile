FROM python:3.6-alpine

ENV APP=goobox-nodes-scraper
ENV BASEDIR=/srv/apps/$APP
ENV APPDIR=$BASEDIR/app
ENV LOGDIR=$BASEDIR/logs
ENV OUTPUTDIR=$BASEDIR/output

ENV PYTHONPATH=$PYTHONPATH:$APPDIR

# Install system dependencies
ENV RUNTIME_PACKAGES libxslt libxml2 jpeg tiff libpng zlib
ENV BUILD_PACKAGES build-base libxslt-dev libxml2-dev libffi-dev jpeg-dev tiff-dev libpng-dev zlib-dev openssl-dev
RUN apk --no-cache add $RUNTIME_PACKAGES

# Create initial dirs
RUN mkdir -p $APPDIR $LOGDIR $OUTPUTDIR
WORKDIR $APPDIR

# Install python requirements
COPY pyproject.toml pyproject.lock $APPDIR/
RUN apk --no-cache add $BUILD_PACKAGES && \
    python -m pip install --upgrade pip poetry && \
    python -m pip install --no-cache-dir --upgrade pip poetry && \
    poetry install && \
    poetry cache:clear pypi --all && \
    apk del $BUILD_PACKAGES

# Copy application
COPY . $APPDIR

ENTRYPOINT ["poetry", "run", "python", "run"]
