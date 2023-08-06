%define pypi_name neutron-arista-ccf-lldp
%define pypi_name_underscore neutron_arista_ccf_lldp

Name:               %{pypi_name}
Version:            1.1.0
Release:            1%{?dist}
Epoch:              1
Summary:            LLDP Agent for Big Switch Networks integration.
License:            ASL 2.0
URL:                https://pypi.python.org/pypi/%{pypi_name}
Source0:            https://pypi.python.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:            neutron-arista-ccf-lldp.service
BuildArch:          noarch

BuildRequires:      python3-pbr
BuildRequires:      python3-setuptools

Requires:           python3-pbr >= 5.1.2
Requires:           python3-oslo-serialization >= 2.29.2
Requires:           os-net-config >= 11.3.2

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
===============================
neutron-arista-ccf-lldp
===============================

LLDP Agent for Big Switch Networks integration.

This program is for python3.6 or later. For python2 version, please check
neutron-bsn-lldp instead.

This custom LLDP agent is used to send LLDPs on interfaces connected to
Big Cloud Fabric (BCF). In environments with os-net-config installed, it reads
config from os-net-config to automagically identify and send LLDPs.

For all other purposes, Big Switch Openstack Installer (BOSI) configures the
service file based on environment info.


%prep
%setup -q -n %{pypi_name}-%{version}

%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/neutron-arista-ccf-lldp.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%license LICENSE
%{python3_sitelib}/%{pypi_name_underscore}
%{python3_sitelib}/*.egg-info
%{_unitdir}/neutron-arista-ccf-lldp.service
%{_bindir}/arista_ccf_lldp

%post
%systemd_post neutron-arista-ccf-lldp.service

%preun
%systemd_preun neutron-arista-ccf-lldp.service

%postun
%systemd_postun_with_restart neutron-arista-ccf-lldp.service

%changelog
* Thu Nov 12 2020 Weifan Fu <weifan.fu@arista.com> - 1.1.0
- initial release created from neutron-bsn-lldp with python3 changes, this version might not be fully functional