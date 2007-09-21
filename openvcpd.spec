Summary:	VServer Control Panel Daemon
Name:		openvcpd
Version:	0.3
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://files.openvcp.org/%{name}-%{version}.tar.gz
# Source0-md5:	2445db39d0728b8169cfb8246b435f30
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-ac.patch
Patch1:		%{name}-DESTDIR.patch
URL:		http://www.openvcp.org/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	autoconf
BuildRequires:	util-vserver-devel
BuildRequires:	sqlite3-devel
BuildRequires:	libxml2-devel
BuildRequires:	libpcap-devel
BuildRequires:	iptables-devel >= 1.3.8-1.1
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
#Provides:	-
#Provides:	group(foo)
#Provides:	user(foo)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VServer Control Panel Daemon.

%prep
%setup -q -n %{name}-%{version}-rc2
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/{rc.d/init.d,sysconfig}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
