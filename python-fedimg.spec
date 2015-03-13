%global modname fedimg

Name:               python-fedimg
Version:            0.5
Release:            1%{?dist}
Summary:            Automatically upload Fedora Cloud images to cloud providers

Group:              Development/Libraries
License:            AGPLv3+
URL:                http://pypi.python.org/pypi/fedimg
Source0:            http://pypi.python.org/packages/source/f/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:          noarch

BuildRequires:      python2-devel
BuildRequires:      python-setuptools
BuildRequires:      python-nose
BuildRequires:      python-mock

BuildRequires:      fedmsg
BuildRequires:      python-libcloud
BuildRequires:      python-paramiko

Requires:           fedmsg
Requires:           python-libcloud
Requires:           python-paramiko


%description
A service that listens to the Fedmsg bus and automatically uploads built Fedora
cloud images to internal and external cloud providers

%prep
%setup -q -n %{modname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info

%build
%{__python} setup.py build

%install

%{__mkdir} -p %{buildroot}%{_sysconfdir}/fedmsg.d/
%{__cp} -p fedimg.cfg.example %{buildroot}%{_sysconfdir}/fedimg.cfg
%{__cp} -p fedmsg.d/fedimg.py %{buildroot}%{_sysconfdir}/fedmsg.d/.

%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

%check
%{__python} setup.py test

%files
%doc docs/ README.md LICENSE
%config(noreplace) %{_sysconfdir}/fedimg.cfg
%config(noreplace) %{_sysconfdir}/fedmsg.d/fedimg.py*

%{python_sitelib}/%{modname}/
%{python_sitelib}/%{modname}-%{version}*

%changelog
* Thu Mar 12 2015 David Gay <dgay@redhat.com> - 0.5.0-1
- new release

* Mon Jan 26 2015 David Gay <dgay@redhat.com> - 0.4.0-1
- new release

* Sun Dec 07 2014 David Gay <dgay@redhat.com> - 0.3.2-1
- new release

* Sat Dec 06 2014 David Gay <dgay@redhat.com> - 0.3.1-1
- new Fedora release
- add python-mock to buildrequires

* Wed Sep 17 2014 David Gay <dgay@redhat.com> - 0.2.6-1
- new version cut after package review
- use proper buildroot macro in spec file
- preserve file timestamps when copying in spec file
- do not make library files executable, and don't give them shebangs
- add license headers to all Python files

* Tue Sep 16 2014 David Gay <dgay@redhat.com> - 0.2.5-1
- initial package for Fedora
