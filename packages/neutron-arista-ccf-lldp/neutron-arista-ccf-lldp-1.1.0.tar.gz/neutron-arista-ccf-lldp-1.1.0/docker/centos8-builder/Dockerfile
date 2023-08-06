FROM centos:centos8
MAINTAINER Weifan Fu <weifan.fu@arista.com>
RUN dnf -y update && yum clean all
RUN dnf groupinstall -y 'Development Tools'
RUN dnf install -y epel-release
RUN dnf install -y python3-pbr
RUN dnf config-manager --enable PowerTools AppStream BaseOS *epel
RUN dnf install -y python3-sphinx
RUN dnf install -y python3-django
RUN dnf install -y python3-devel
RUN dnf install -y python3-d2to1
RUN dnf install -y python3-lockfile
RUN pip3 install -U eventlet
RUN dnf install -y python3-six
RUN dnf install -y python3-netaddr
RUN dnf install -y python3-kombu
RUN dnf install -y python3-anyjson
RUN dnf install -y python3-iso8601
RUN pip3 install -U twine
