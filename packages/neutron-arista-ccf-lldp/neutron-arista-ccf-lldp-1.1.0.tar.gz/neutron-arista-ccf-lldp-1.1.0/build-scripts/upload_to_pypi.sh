#!/bin/bash
# Copyright 2018 Big Switch Networks, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
set -eux

# RPM runs as root and doesn't like source files owned by a random UID
OUTER_UID=$(stat -c '%u' /neutron-bsn-lldp)
OUTER_GID=$(stat -c '%g' /neutron-bsn-lldp)
trap "chown -R $OUTER_UID:$OUTER_GID /neutron-bsn-lldp" EXIT
chown -R root:root /neutron-bsn-lldp

cd /neutron-bsn-lldp
git config --global user.name "Big Switch Networks"
git config --global user.email "support@bigswitch.com"

CURR_VERSION=$(awk '/^version/{print $3}' setup.cfg)

echo 'CURR_VERSION=' $CURR_VERSION
git tag -f -s $CURR_VERSION -m $CURR_VERSION -u "Big Switch Networks"

python3 setup.py sdist

# force success. but always check if pip install fails
twine upload dist/* -r pypi -s -i "Big Switch Networks" || true
# delay of 30 seconds
sleep 30
pip3 install --upgrade neutron-arista-ccf-lldp==$CURR_VERSION

if [ "$?" -eq "0" ]
then
  echo "PYPI upload successful."
else
  echo "PYPI upload FAILED. Check the logs."
fi
# remove the package
pip3 uninstall -y neutron-arista-ccf-lldp

# revert the permissions of the repo folder
chown -R $OUTER_UID:$OUTER_GID /neutron-bsn-lldp
