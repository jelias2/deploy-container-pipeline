FROM jenkins/jenkins:lts
LABEL maintainer="GaRgAm"
USER root

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
      apt-transport-https \
      ca-certificates \
      jq \
      curl \
      gnupg2 \
      less \
      groff \
      software-properties-common && \
    apt-get install -y \
      python-pip && \
    curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey; apt-key add /tmp/dkey && \
    add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
      $(lsb_release -cs) \
      stable" && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
      docker-ce && \
    pip install awscli --upgrade && \
    rm -rf /var/lib/apt/lists/*
