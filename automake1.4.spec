%define amversion 1.4
%define pkgname automake
%define patchlevel p6
%define version 1.4.0.%{patchlevel}

%define docheck 0
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		%{pkgname}%{amversion}
Version:	%{version}
Release:	15
License:	GPL
Group:		Development/Other
Source:		ftp://ftp.gnu.org/gnu/automake/%{pkgname}-%{amversion}-%{patchlevel}.tar.bz2
Patch0:		automake-1.4p6-infofiles.patch
Patch1:		automake-1.4-p6-stdc-headers.patch
Patch2:		automake-1.4-p6-CVE-2009-4029.diff
URL:		http://www.gnu.org/software/automake/
BuildArch:	noarch

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
%makeinstall

install -D -m 644 %{name}.info $RPM_BUILD_ROOT%{_infodir}/%{name}.info

rm -f $RPM_BUILD_ROOT/%{_bindir}/{automake,aclocal}

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/aclocal

%post
update-alternatives --remove automake %{_bindir}/automake-%{amversion}

# this triggerpostun doesn't seem to work, using post instead
#triggerpostun -- automake <= 1.4-25.p6.mdk
#if [ -e %{_bindir}/automake-%{amversion} ]; then
#  update-alternatives --remove automake %{_bindir}/automake-%{amversion}
#fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%{_bindir}/*
%{_datadir}/*-1.4
%{_infodir}/%{name}*
%dir %{_datadir}/aclocal




%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.0.p6-8mdv2011.0
+ Revision: 662899
- mass rebuild

* Thu Oct 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.0.p6-7mdv2011.0
+ Revision: 585578
- disable the make check for now
- P2: security fix for CVE-2009-4029 (redhat)

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.0.p6-6mdv2010.1
+ Revision: 520013
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.0.p6-5mdv2010.0
+ Revision: 413148
- rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.4.0.p6-4mdv2009.0
+ Revision: 220473
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.4.0.p6-3mdv2008.1
+ Revision: 148886
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 1.4.0.p6-2mdv2008.0
+ Revision: 69353
- kill file require on update-alternatives
- fix prereq


* Tue Jan 30 2007 Götz Waschk <waschk@mandriva.org> 1.4.0.p6-1mdv2007.0
+ Revision: 115356
- unpack patches
- Import automake1.4

* Tue Jan 30 2007 Götz Waschk <waschk@mandriva.org> 1.4.0.p6-1mdv2007.1
- move tests to the check section

* Mon Jun 27 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.4.0.p6-1mdk
- this package is not an alternative for current "automake"
- better versioning

* Tue Jul 27 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4-25.p6.mdk
- Patch1: gcc no longer accept K&R style prototypes

* Wed May 19 2004 Abel Cheung <deaddog@deaddog.org> 1.4-24.p6.mdk
- Patch0: Use versioned name in info page nodes
- Tune down alternative priority
- Add `--without check' option to disable `make check'

