%define amversion 1.4
%define pkgname automake
%define patchlevel p6
%define version 1.4.0.%{patchlevel}
%define release %mkrel 7

%define docheck 0
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		%{pkgname}%{amversion}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source:		ftp://ftp.gnu.org/gnu/automake/%{pkgname}-%{amversion}-%{patchlevel}.tar.bz2
Patch0:		automake-1.4p6-infofiles.patch
Patch1:		automake-1.4-p6-stdc-headers.patch
Patch2:		automake-1.4-p6-CVE-2009-4029.diff
URL:		http://www.gnu.org/software/automake/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch

Requires(post):	info-install
Requires(preun):	info-install
Requires:	update-alternatives
Conflicts:	automake1.5
Obsoletes:	automake <= 1.4-23.p6.mdk

%description
Automake is a tool for automatically generating Makefiles compliant with the
GNU Coding Standards.

You should install Automake if you are developing software and would like to
use its capabilities of automatically generating GNU standard Makefiles. If you
install Automake, you will also need to install GNU's Autoconf package.

%prep
%setup -q -n %{pkgname}-%{amversion}-%{patchlevel}
%patch0 -p1 -b .parallel
%patch1 -p1 -b .gcc3.4
%patch2 -p1 -b .CVE-2009-4029

%build
%configure
%make

# error.test won't work as expected because $ACLOCAL already include ./m4 into
# m4 file search list (see tests/defs), so --acdir=. has no effect
perl -pi -e 's/\berror\.test\b//' tests/Makefile

# (oe) the installsh.test test fails, don't know why
%check
%if %docheck
make check	# VERBOSE=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

install -D -m 644 %{name}.info $RPM_BUILD_ROOT%{_infodir}/%{name}.info

rm -f $RPM_BUILD_ROOT/%{_bindir}/{automake,aclocal}

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/aclocal

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}.info
update-alternatives --remove automake %{_bindir}/automake-%{amversion}

# this triggerpostun doesn't seem to work, using post instead
#triggerpostun -- automake <= 1.4-25.p6.mdk
#if [ -e %{_bindir}/automake-%{amversion} ]; then
#  update-alternatives --remove automake %{_bindir}/automake-%{amversion}
#fi

%preun
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%{_bindir}/*
%{_datadir}/*-1.4
%{_infodir}/%{name}*
%dir %{_datadir}/aclocal


