%define name              ligo-gracedb
%define version           2.7.2
%define unmangled_version 2.7.2
%define release           1

Summary:   Gravity Wave Candidate Event Database
Name:      %{name}
Version:   %{version}
Release:   %{release}%{?dist}
Source0:   https://pypi.io/packages/source/l/%{name}/%{name}-%{unmangled_version}.tar.gz
License:   GPLv3+
Group:     Development/Libraries
Prefix:    %{_prefix}
Vendor:    Tanner Prestegard <tanner.prestegard@ligo.org>, Alexander Pace <alexander.pace@ligo.org>
Url:       http://www.lsc-group.phys.uwm.edu/daswg/gracedb.html

BuildArch: noarch

# srpm dependencies:
BuildRequires: python-srpm-macros
# build macro dependencies:
BuildRequires: python2-rpm-macros
BuildRequires: python3-rpm-macros

# build dependencies:
BuildRequires: python
BuildRequires: python%{python3_pkgversion}
BuildRequires: python-setuptools
BuildRequires: python%{python3_pkgversion}-setuptools

%description
The gravitational-wave candidate event database (GraceDB) is a prototype
system to organize candidate events from gravitational-wave searches and
to provide an environment to record information about follow-ups. A simple
client tool is provided to submit a candidate event to the database.

# -- python2-ligo-gracedb

%package -n python2-%{name}
Summary:  %{summary}
Provides: %{name}
Obsoletes: %{name}
Requires: python-six
Requires: python2-ligo-common
Requires: python-future
Requires: python2-cryptography
Requires: python-requests

%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
The gravitational-wave candidate event database (GraceDB) is a prototype
system to organize candidate events from gravitational-wave searches and
to provide an environment to record information about follow-ups. A simple
client tool is provided to submit a candidate event to the database.

# -- python-3X-ligo-gracedb

%package -n python%{python3_pkgversion}-%{name}
Summary:  %{summary}
Requires: python%{python3_pkgversion}-six
Requires: python%{python3_pkgversion}-ligo-common
Requires: python%{python3_pkgversion}-future
Requires: python%{python3_pkgversion}-cryptography

%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

%description -n python%{python3_pkgversion}-%{name}
The gravitational-wave candidate event database (GraceDB) is a prototype
system to organize candidate events from gravitational-wave searches and
to provide an environment to record information about follow-ups. A simple
client tool is provided to submit a candidate event to the database.

# -- build steps

%prep
%setup -n %{name}-%{unmangled_version}

%build
%py2_build
%py3_build

%install
# install python3 first
%py3_install
# so that the scripts come from python2
%py2_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python2-%{name}
%license LICENSE
%{_bindir}/gracedb
%{_bindir}/gracedb_legacy
%{python2_sitelib}/*

%files -n python%{python3_pkgversion}-%{name}
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Jun 12 2019 Duncan Macleod <duncan.macleod@ligo.org> 2.2.2-2
- fixed incorrect installation of /usr/bin/ scripts
- cleaned up spec file
