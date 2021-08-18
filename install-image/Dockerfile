FROM registry.access.redhat.com/ubi8/ubi:8.4-209
LABEL \
  maintainer="kin.wai.koo@gmail.com" \
  io.k8s.description="Installation image"
ARG OC_VERSION=4.7

RUN \
  yum update -y \
  && \
  yum install -y git make jq \
  && \
  curl -o /tmp/oc.tgz https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/latest-${OC_VERSION}/openshift-client-linux.tar.gz \
  && \
  cd /usr/local/bin \
  && \
  tar -zxf /tmp/oc.tgz \
  && \
  rm -f /tmp/oc.tgz
