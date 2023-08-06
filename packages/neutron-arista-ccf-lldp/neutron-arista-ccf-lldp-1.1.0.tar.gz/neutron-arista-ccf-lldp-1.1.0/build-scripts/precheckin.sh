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
#!/bin/bash -eux

# switch to git repo directory inside container
cd /neutron-bsn-lldp

pwd
echo 'git commit is' ${GIT_COMMIT}

tox -e pep8

setup_cfg_modified=`git log -m -1 --name-only --pretty="format:" | grep setup.cfg | wc -l`
if [ ${setup_cfg_modified} -lt 1 ];
  then echo "Update setup.cfg with new version number. Build FAILED";
  exit 1;
else
  echo "setup.cfg updated"; fi
# check the new_version > old_version
echo 'checking if version bump is correct'
git log -m -1 ${GIT_COMMIT} --pretty="format:" -p setup.cfg | grep version | python3 build-scripts/is_version_bumped.py

CURR_VERSION=$(awk '/^version/{print $3}' setup.cfg)
SPEC_VERSION=$(awk '/^Version/{print $2}' rhel/neutron-arista-ccf-lldp.spec)

if [ "$CURR_VERSION" != "$SPEC_VERSION" ];
  then echo "Update python-neutron-arista-ccf-lldp.spec with new version number. Build FAILED."
  exit 1;
else
  echo "neutron-arista-ccf-lldp.spec updated correctly"; fi
