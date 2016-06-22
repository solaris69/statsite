%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:		statsite
Version:	0.7.1
Release:	10%{?dist}
Summary:	A C implementation of statsd.
Group:		Applications
License:	See the LICENSE file.
URL:		https://github.com/armon/statsite
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	scons check-devel %{?el7:systemd} %{?fedora:systemd}
AutoReqProv:	No
Requires(pre):  shadow-utils

%define compass_mon_app /compass/monitor/app
%define compass_mon_cfg /compass/monitor/cfg
%define compass_mon_log /compass/monitor/log

%description

Statsite is a metrics aggregation server. Statsite is based heavily on Etsy\'s StatsD
https://github.com/etsy/statsd, and is wire compatible.

%prep
%setup

%build
cd /vagrant
make %{?_smp_mflags}

%install
mkdir -vp $RPM_BUILD_ROOT/%{compass_mon_app}/statsite
mkdir -vp $RPM_BUILD_ROOT/%{compass_mon_cfg}/statsite
mkdir -vp $RPM_BUILD_ROOT/%{compass_mon_app}/statsite/sinks
mkdir -vp $RPM_BUILD_ROOT/%{compass_mon_app}/statsite/share
mkdir -vp $RPM_BUILD_ROOT/%{compass_mon_log}/statsite
mkdir -vp $RPM_BUILD_ROOT/etc/init.d
mkdir -vp $RPM_BUILD_ROOT/var/run/%{name}

%if 0%{?fedora}%{?el7}
mkdir -vp $RPM_BUILD_ROOT/%{_unitdir}
install -m 644 rpm/statsite.service $RPM_BUILD_ROOT/%{_unitdir}
install -m 644 rpm/statsite.tmpfiles.conf $RPM_BUILD_ROOT/etc/tmpfiles.d/statsite.conf
%else
install -m 755 /vagrant/rpm/statsite.initscript $RPM_BUILD_ROOT/etc/init.d/statsite
%endif

install -m 755 /vagrant/src/statsite $RPM_BUILD_ROOT/%{compass_mon_app}/statsite/statsite
install -m 644 /vagrant/rpm/statsite.conf.example $RPM_BUILD_ROOT/%{compass_mon_cfg}/statsite/statsite.conf
cp -a /vagrant/sinks $RPM_BUILD_ROOT/%{compass_mon_app}/statsite
cp -a /vagrant/{LICENSE,CHANGELOG.md,README.md} $RPM_BUILD_ROOT/%{compass_mon_app}/statsite/share
cp -a /vagrant/rpm/statsite.conf.example $RPM_BUILD_ROOT/%{compass_mon_app}/statsite/share

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
if [ "$1" = 1 ] ; then
%if 0%{?fedora}%{?el7}
	systemctl daemon-reload
%else
	/sbin/chkconfig --add %{name}
	/sbin/chkconfig %{name} off
%endif

fi
exit 0

%postun
if [ "$1" = 1 ] ; then
%if 0%{?fedora}%{?el7}
	systemctl restart statsite.service
%else
	/sbin/service %{name} restart

%endif
fi
exit 0

%preun
if [ "$1" = 0 ] ; then
	%if 0%{?monit_bin}
	%{monit_bin} stop %{name}
	%endif

%if 0%{?fedora}%{?el7}
	systemctl stop statsite.service
%else
	/sbin/service %{name} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{name}
%endif
fi
exit 0

%files
%defattr(-,root,root,-)
%doc %{compass_mon_app}/statsite/share/LICENSE
%doc %{compass_mon_app}/statsite/share/CHANGELOG.md
%doc %{compass_mon_app}/statsite/share/README.md
%doc %{compass_mon_app}/statsite/share/statsite.conf.example
%config %{compass_mon_cfg}/statsite/statsite.conf
%attr(755, root, root) %{compass_mon_app}/statsite/statsite
%if 0%{?fedora}%{?el7}
%attr(644, root, root) %{_unitdir}/statsite.service
%dir /etc/tmpfiles.d
%attr(644, root, root) /etc/tmpfiles.d/statsite.conf
%else
%attr(755, root, root) /etc/init.d/statsite
%endif
%dir %{compass_mon_app}/statsite
%dir %{compass_mon_app}/statsite/sinks
%attr(755, statsite, statsite) %{compass_mon_app}/statsite/statsite
%attr(755, root, root) %{compass_mon_app}/statsite/sinks/__init__.py
%attr(755, root, root) %{compass_mon_app}/statsite/sinks/binary_sink.py
%attr(755, root, root) %{compass_mon_app}/statsite/sinks/librato.py
%attr(755, root, root) %{compass_mon_app}/statsite/sinks/statsite_json_sink.rb
%attr(755, root, root) %{compass_mon_app}/statsite/sinks/gmetric.py
%attr(755, root, root) %{compass_mon_app}/statsite/sinks/influxdb.py
%attr(755, root, root) %{compass_mon_app}/statsite/sinks/graphite.py
%attr(755, root, root) %{compass_mon_app}/statsite/sinks/cloudwatch.sh
%attr(755, root, root) %{compass_mon_app}/statsite/sinks/opentsdb.js

%changelog
* Mon Jun 20 2016 Verachan Man-in <vmanin@outlook.com> - 0.7.1-10
- Remove a statsite user and group. I use compass instead.
- Move installed location to /compass/monitor/app and configuration location to /compass/monitor/cfg

* Tue May 12 2015 Yann Ramin <yann@twitter.com> - 0.7.1-1
- Add a statsite user and group
- Add systemd support

* Fri Jul 18 2014 Gary Richardson <gary.richardson@gmail.com>
- added missing __init__.py to spec file
- fixed makefile for building RPMS

* Tue May 20 2014 Marcelo Teixeira Monteiro <marcelotmonteiro@gmail.com>
- Added initscript and config file
- small improvements

* Wed Nov 20 2013 Vito Laurenza <vitolaurenza@hotmail.com>
- Added 'sinks', which I overlooked initially.

* Fri Nov 15 2013 Vito Laurenza <vitolaurenza@hotmail.com>
- Initial release.
