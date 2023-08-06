Name: libsigscan
Version: 20201117
Release: 1
Summary: Library for binary signature scanning
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libsigscan
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
          
BuildRequires: gcc          

%description -n libsigscan
Library for binary signature scanning

%package -n libsigscan-static
Summary: Library for binary signature scanning
Group: Development/Libraries
Requires: libsigscan = %{version}-%{release}

%description -n libsigscan-static
Static library version of libsigscan.

%package -n libsigscan-devel
Summary: Header files and libraries for developing applications for libsigscan
Group: Development/Libraries
Requires: libsigscan = %{version}-%{release}

%description -n libsigscan-devel
Header files and libraries for developing applications for libsigscan.

%package -n libsigscan-python2
Obsoletes: libsigscan-python < %{version}
Provides: libsigscan-python = %{version}
Summary: Python 2 bindings for libsigscan
Group: System Environment/Libraries
Requires: libsigscan = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libsigscan-python2
Python 2 bindings for libsigscan

%package -n libsigscan-python3
Summary: Python 3 bindings for libsigscan
Group: System Environment/Libraries
Requires: libsigscan = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libsigscan-python3
Python 3 bindings for libsigscan

%package -n libsigscan-tools
Summary: Several tools for binary signature scanning files
Group: Applications/System
Requires: libsigscan = %{version}-%{release}

%description -n libsigscan-tools
Several tools for binary signature scanning files

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libsigscan
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libsigscan-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libsigscan-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libsigscan.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libsigscan-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libsigscan-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libsigscan-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%config %{_sysconfdir}/sigscan.conf

%changelog
* Tue Nov 17 2020 Joachim Metz <joachim.metz@gmail.com> 20201117-1
- Auto-generated

