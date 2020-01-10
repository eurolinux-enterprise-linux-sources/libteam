Name: libteam
Version: 1.27
Release: 5%{?dist}
Summary: Library for controlling team network device
Group: System Environment/Libraries
License: LGPLv2+
URL: http://www.libteam.org
Source: http://www.libteam.org/files/libteam-%{version}.tar.gz
Patch1: libteam-teamd-do-not-process-lacpdu-before-the-port-ifinfo-i.patch
Patch2: libteam-teamd-add-port_hwaddr_changed-for-ab-runner.patch
Patch3: libteam-teamd-add-port_hwaddr_changed-for-lb-runner.patch
Patch4: libteam-teamd-add-port_hwaddr_changed-for-lacp-runner.patch
Patch5: libteam-man-fix-runner.sys_prio-default.patch
Patch6: libteam-configure.ac-Empty-LDFLAGS-before-checking-for-libnl.patch
Patch7: libteam-libteam-don-t-crash-when-trying-to-print-unregistere.patch
BuildRequires: jansson-devel
BuildRequires: libdaemon-devel
BuildRequires: libnl3-devel
BuildRequires: python-devel
BuildRequires: dbus-devel
BuildRequires: swig
BuildRequires: doxygen
BuildRequires: autoconf automake libtool

%description
This package contains a library which is a user-space
counterpart for team network driver. It provides an API
to control team network devices.

%package devel
Group: Development/Libraries
Summary: Libraries and header files for libteam development
Requires: libteam = %{version}-%{release}

%package doc
Group: Documentation
Summary: API documentation for libteam and libteamd
Requires: libteam = %{version}-%{release}

%package -n teamd
Group: System Environment/Daemons
Summary: Team network device control daemon
Requires: libteam = %{version}-%{release}

%package -n teamd-devel
Group: Development/Libraries
Summary: Libraries and header files for teamd development
Requires: teamd = %{version}-%{release}

%package -n python-libteam
Group: Development/Libraries
Summary: Team network device library bindings
Requires: libteam = %{version}-%{release}

%description devel
The libteam-devel package contains the header files and libraries
necessary for developing programs using libteam.

%description doc
This package contains libteam and libteamd API documentation

%description -n teamd
The teamd package contains team network device control daemon.

%description -n teamd-devel
The teamd-devel package contains the header files and libraries
necessary for developing programs using libteamdctl.

%description -n python-libteam
The team-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by team network device library.

This package should be installed if you want to develop Python
programs that will manipulate team network devices.

%define _hardened_build 1

%prep
%autosetup -p1
autoreconf --force --install -I m4

# prepare example dir for -devel
mkdir -p _tmpdoc1/examples
cp -p examples/*.c _tmpdoc1/examples
# prepare example dir for team-python
mkdir -p _tmpdoc2/examples
cp -p examples/python/*.py _tmpdoc2/examples
chmod -x _tmpdoc2/examples/*.py

%build
%configure --disable-static
make %{?_smp_mflags}
make html
cd binding/python
python ./setup.py build

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name \*.la -delete
rm -rf $RPM_BUILD_ROOT/%{_bindir}/team_*
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d
install -p teamd/dbus/teamd.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p teamd/redhat/systemd/teamd@.service $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-Team $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-Team $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-TeamPort $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-TeamPort $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 utils/bond2team $RPM_BUILD_ROOT%{_bindir}/bond2team
cd binding/python
python ./setup.py install --root $RPM_BUILD_ROOT -O1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libteam.so.*
%{_bindir}/teamnl
%{_mandir}/man8/teamnl.8*

%files devel
%doc COPYING _tmpdoc1/examples
%{_includedir}/team.h
%{_libdir}/libteam.so
%{_libdir}/pkgconfig/libteam.pc

%files doc
%doc COPYING doc/api

%files -n teamd
%doc COPYING teamd/example_configs teamd/redhat/example_ifcfgs/
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/teamd.conf
%config(noreplace) %attr(644,root,root) %{_unitdir}/teamd@.service
%{_sysconfdir}/sysconfig/network-scripts/ifup-Team
%{_sysconfdir}/sysconfig/network-scripts/ifdown-Team
%{_sysconfdir}/sysconfig/network-scripts/ifup-TeamPort
%{_sysconfdir}/sysconfig/network-scripts/ifdown-TeamPort
%{_libdir}/libteamdctl.so.*
%{_bindir}/teamd
%{_bindir}/teamdctl
%{_bindir}/bond2team
%{_mandir}/man8/teamd.8*
%{_mandir}/man8/teamdctl.8*
%{_mandir}/man5/teamd.conf.5*
%{_mandir}/man1/bond2team.1*

%files -n teamd-devel
%doc COPYING
%{_includedir}/teamdctl.h
%{_libdir}/libteamdctl.so
%{_libdir}/pkgconfig/libteamdctl.pc

%files -n python-libteam
%doc COPYING _tmpdoc2/examples
%{python_sitearch}/*

%changelog
* Fri May 18 2018 Xin Long <lxin@redhat.com> - 1.27-5
- Added patch to fix runner.sys_prio default in man docs [1533813]
- Added patch to empty LDFLAGS before checking for libnl3 in configure.ac [1533847]
- Added patch to not crash when trying to print unregistered device name [1563155]

* Fri Feb 9 2018 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.27-4
- Add port_hwaddr_changed for ab, lb and lacp runners [1499063]

* Wed Feb 7 2018 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.27-3
- Added fix to only process LACPDU after port ifinfo is set [1493600]

* Mon Aug 21 2017 Xin Long <lxin@redhat.com> - 1.27-2
- Updated to 1.27 [1445499 1440866 1486935]

* Fri Mar 24 2017 Xin Long <lxin@redhat.com> - 1.25-5
- Added patch to escape some sensitive characters [1383997]
- Added patch to check port link_up when a port is added for lb runner
  [1393430]

* Wed Aug 17 2016 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.25-4
- Added patches to avoid hung on shutdown [1330550]
- Added patch to fix an out-of-bound write with zero-length hardware
  address [1286840]

* Thu Jun 23 2016 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.25-2
- Updated to 1.25 [1286840 1286063]
- Added patch teamd-LACP-runner-does-not-set-Agg-bit-on-first-slav.patch [1347818]

* Wed Jan 20 2016 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.23-1
- Updated to 1.23 [1286840 1273052]

* Fri Dec 11 2015 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.22-1
- Updated to 1.22 [1286840]

* Wed Dec 02 2015 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.17-6
- Added patch Fix sending duplicate LACP frames at the start [1267494]

* Fri Sep 11 2015 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.17-5
- Added patch fixing typo on delay_up [1242628]

* Tue Sep 01 2015 Xin Long <lxin@redhat.com> - 1.17-4
- Added patch change actor system value on team mac change in lacp [1253769]

* Tue Sep 01 2015 Xin Long <lxin@redhat.com> - 1.17-3
- Added patch fixing the lack of hwaddr_changed for loadbalance mode [1255458]

* Fri Aug 28 2015 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.17-2
- Added patch fixing select parameter [1257195]

* Fri Apr 03 2015 Jiri Pirko <jpirko@redhat.com> - 1.17-1
- rebase to version 1.17 [1208418 1208414 1190102 1166863 1166864 1203611 1206483]

* Wed Dec 17 2014 Jiri Pirko <jpirko@redhat.com> - 1.15-1
- rebase to version 1.15 [1116970 1173632]

* Wed Nov 05 2014 Jiri Pirko <jpirko@redhat.com> - 1.14-1
- rebase to version 1.14 [1116970]

* Wed Nov 05 2014 Jiri Pirko <jpirko@redhat.com> - 1.13-1
- rebase to version 1.13 [1116970 1160615]

* Wed Aug 20 2014 Jiri Pirko <jpirko@redhat.com> - 1.12-1
- rebase to version 1.12 [1116970 1125296]

* Thu Jul 31 2014 Jiri Pirko <jpirko@redhat.com> - 1.11-1
- rebase to version 1.11 [1116970 1072855 1082522 1082551 1085938 1086383 1089256 1090578 1092549]

* Mon Mar 31 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-15
- teamdctl: unmess check_teamd_team_devname and fix double free there [1078099]

* Fri Mar 28 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-14
- teamd_link_watch: allow to send ARP probes if no source_host is specified [1078993]
- bond2team: do not guess source_host option [1079059]
- teamd_link_watch: specify "missed_max" option default value [1079059]
- man: correct type of "*_host" options [1078993]

* Thu Mar 27 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-13
- teamdctl: add command for easy port presention checking [1081214]
- initscripts: do not try to re-add port if it is already there [1081214]

* Fri Mar 07 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-12
- libteamdctl: add notice for caller to do not modify [1072620]

* Fri Mar 07 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-11
- usock: accept multiline message string parameters [1051517]

* Wed Feb 26 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-10
- fix port handling when "take over" option is on [1070065]

* Fri Feb 21 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-9
- spec: remove patch backup files

* Fri Feb 21 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-8
- teamd: fixed couple comments [1067851]
- teamd: update hwaddr when changing team's macaddr [1067851]
- redhat: fix boolean types in example 2 [1067851]

* Wed Feb 12 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-7
- initscripts: fix port up before master and port down after master [1062675]

* Mon Feb 03 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-6
- lb: enable/disable port according to linkwatch state [1057223]

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.9-5
- Mass rebuild 2014-01-24

* Thu Jan 23 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-4
- fix multilib [983267]

* Tue Jan 21 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-3
- man teamdctl: Minor improvements to style and language [1055940]
- man teamd.conf: Minor improvements to style and language [1055940]
- fix comment typo in ifdown-Team scripts [1035173]

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.9-2
- Mass rebuild 2013-12-27

* Wed Nov 13 2013 Jiri Pirko <jpirko@redhat.com> - 1.9-1
- Rebase to 1.9
- libteamdctl: remove false lib dependencies
- teamdctl: use new port config get function
- libteamdctl: introduce support for port config get
- libteamdctl: cache reply strings into list
- teamd: introduce PortConfigDump control method
- teamd: make teamd_get_port_by_ifname ifname argument const
- Minor improvements to style and language.
- do not install example binaries
- minor man page(s) correction(s) and lintianisation
- teamdctl: print error message if ifindex cannot be obtained
- fix cflags path in pc files
Resolves: rhbz#1028138
Resolves: rhbz#1013640
Resolves: rhbz#1029186

* Tue Aug 13 2013 Jiri Pirko <jpirko@redhat.com> - 1.8-1
- Rebase to 1.8

* Tue Jun 11 2013 Jiri Pirko <jpirko@redhat.com> - 1.3-1
- Update to 1.3

* Wed May 29 2013 Jiri Pirko <jpirko@redhat.com> - 1.2-1
- Update to 1.2

* Thu May 16 2013 Jiri Pirko <jpirko@redhat.com> - 1.1-1
- Update to 1.1

* Thu Jan 31 2013 Jiri Pirko <jpirko@redhat.com> - 1.0-1
- Update to 1.0

* Sun Jan 20 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-27.20130110gitf16805c
- Rebuilt for libnl3

* Sun Jan 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.1-26.20130110gitf16805c
- Rebuilt for libnl3

* Thu Jan 10 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-25.20130110gitf16805c
- Rebase to git commit f16805c

* Wed Dec 12 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-24.20121212git01fe4bd
- Rebase to git commit 01fe4bd

* Thu Dec 06 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-23.20121206git659a848
- Rebase to git commit 659a848

* Thu Nov 22 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-22.20121122git18b6701
- Rebase to git commit 18b6701

* Thu Nov 15 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-21.20121115gitffb5267
- Rebase to git commit ffb5267

* Mon Nov 05 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-20.20121105git3b95b34
- Rebase to git commit 3b95b34

* Thu Oct 25 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-19.20121025git7fe7c72
- Rebase to git commit 7fe7c72

* Fri Oct 19 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-18.20121019git1a91059
- Rebase to git commit 1a91059

* Sun Oct 07 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-17.20121007git6f48751
- Rebase to git commit 6f48751

* Tue Sep 25 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-16.20120925gitcc5cddc
- Rebase to git commit cc5cddc

* Sun Sep 23 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-15.20120923git8448186
- Rebase to git commit 8448186

* Tue Sep 04 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-14.20120904gitbdcf72c
- Rebase to git commit bdcf72c

* Wed Aug 22 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-13.20120822gitc0d943d
- Rebase to git commit c0d943d

* Tue Aug 07 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-12.20120807git9fa4a96
- Rebase to git commit 9fa4a96

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-11.20120628gitca7b526
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-10.20120628gitca7b526
- Rebase to git commit ca7b526

* Wed Jun 27 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-9.20120627git96569f8
- Rebase to git commit 96569f8

* Wed Jun 27 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-8.20120627gitcd6b557
- Rebase to git commit cd6b557

* Wed Jun 20 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-7.20120620gita88fabf
- Rebase to git commit a88fabf

* Fri May 04 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-6.20120504git11e234a
- Rebase to git commit 11e234a

* Thu Apr 05 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-5.20120405gita82f8ac
- Rebase to git commit a82f8ac

* Tue Feb 21 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-4.20120221gitfe97f63
- Rebase to git commit fe97f63

* Mon Jan 30 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-3.20120130gitb5cf2a8
- Rebase to git commit b5cf2a8

* Wed Jan 25 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-2.20120125gita1718f8
- Rebase to git commit a1718f8

* Wed Jan 18 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-1.20120113git302672e
- Initial build.
