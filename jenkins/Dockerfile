FROM jenkins/jenkins:lts-jdk11
# if we want to install via apt
ARG PROXY
USER root
RUN sed -i.bak 's/deb.debian.org/mirror.yandex.ru/' /etc/apt/sources.list && \
    if [ -z "PROXY" ]; \
      then echo "Using no PROXY" 1>&2; \
      else echo 'Acquire::http { Proxy "'"$PROXY"'"; };' >/etc/apt/apt.conf.d/99-proxy; \
    fi && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
            firefox-esr python3-venv xvfb \
            build-essential libssl-dev libffi-dev && \
    if [ !-z "PROXY" ]; \
      then rm -f /etc/apt/apt.conf.d/99-proxy; \
    fi && \
    curl -sOL https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-linux64.tar.gz && \
    tar -C /usr/bin -xzf geckodriver-v0.32.2-linux64.tar.gz && \
    rm geckodriver-v0.32.2-linux64.tar.gz && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g phantomjs-prebuilt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# drop back to the regular jenkins user - good practice
USER jenkins
