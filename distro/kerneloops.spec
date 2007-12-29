Name:           kerneloops
Version:        0.7
Release:        1%{?dist}
Summary:        Tool to automatically collect and submit kernel crash signatures

Group:          System Environment/Base
License:        GPLv2
URL:            http://www.kerneloops.org
Source0:        http://www.kerneloops.org/download/%{name}-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  curl-devel
Requires(post): chkconfig
Requires(preun): chkconfig, initscripts
Requires(postun): initscripts

%package defaulton
Summary:        Tool to automatically collect and submit kernel crash signatures
Group:          System Environment/Base
License:        GPLv2

%description
This package contains the tools to collect kernel crash signatures,
and to submit them to the kerneloops.org website where the kernel
crash signatures get collected and groups for presentation to the
Linux kernel developers.

%description defaulton
This package contains the tools to collect kernel crash signatures,
and to submit them to the kerneloops.org website where the kernel
crash signatures get collected and groups for presentation to the
Linux kernel developers.


%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%check
# re-enable when upstream fixes this
# make tests

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -m 0755 -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d
install -p -m 0755 kerneloops.init $RPM_BUILD_ROOT%{_sysconfdir}/init.d/kerneloops

%clean
make clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1"  ]; then
        /sbin/chkconfig --add kerneloops
fi

%preun
if [ "$1" = "1" ]; then
        /sbin/service kerneloops stop > /dev/null 2>&1
        /sbin/chkconfig --del kerneloops
fi

%post defaulton
sed -i -e "s/allow-submit = no/allow-submit = yes/" /etc/kerneloops.conf
if [ "$1" = "1"  ]; then
        /sbin/chkconfig --add kerneloops
fi

%preun defaulton
if [ "$1" = "1" ]; then
        /sbin/service kerneloops stop > /dev/null 2>&1
        /sbin/chkconfig --del kerneloops
fi

%files
%defattr(-,root,root)
%doc COPYING Changelog
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/kerneloops.conf
%{_sysconfdir}/init.d/kerneloops


%files defaulton
%defattr(-,root,root)
%doc COPYING Changelog
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/kerneloops.conf
%{_sysconfdir}/init.d/kerneloops



%changelog
* Sat Dec 29 2008 Arjan van de Ven <arjan@linux.intel.com> - 0.7-1
- fix memory leak
* Wed Dec 19 2008 Arjan van de Ven <arjan@linux.intel.com> - 0.6-1
- various cleanups and minor improvements
- Merged Matt Domsch's improvements
* Tue Dec 18 2008 Arjan van de Ven <arjan@linux.intel.com> - 0.5-1
- fix infinite loop
* Mon Dec 17 2008 Arjan van de Ven <arjan@linux.intel.com> - 0.4-1
- PPC bugfixes
* Sun Dec 9 2008 Arjan van de Ven <arjan@linux.intel.com> - 0.3-1
- more fixes
* Sat Dec 8 2008 Arjan van de Ven <arjan@linux.intel.com> - 0.2-1
- bugfix to submit the whole oops on x86
* Sat Dec 1 2008 Arjan van de Ven <arjan@linux.intel.com> - 0.1-1
- Initial packaging
