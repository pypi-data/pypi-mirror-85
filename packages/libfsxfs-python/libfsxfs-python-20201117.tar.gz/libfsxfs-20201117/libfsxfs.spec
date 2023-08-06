Name: libfsxfs
Version: 20201117
Release: 1
Summary: Library to support the X File System (XFS) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfsxfs
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
              
BuildRequires: gcc              

%description -n libfsxfs
Library to support the X File System (XFS) format

%package -n libfsxfs-static
Summary: Library to support the X File System (XFS) format
Group: Development/Libraries
Requires: libfsxfs = %{version}-%{release}

%description -n libfsxfs-static
Static library version of libfsxfs.

%package -n libfsxfs-devel
Summary: Header files and libraries for developing applications for libfsxfs
Group: Development/Libraries
Requires: libfsxfs = %{version}-%{release}

%description -n libfsxfs-devel
Header files and libraries for developing applications for libfsxfs.

%package -n libfsxfs-python2
Obsoletes: libfsxfs-python < %{version}
Provides: libfsxfs-python = %{version}
Summary: Python 2 bindings for libfsxfs
Group: System Environment/Libraries
Requires: libfsxfs = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libfsxfs-python2
Python 2 bindings for libfsxfs

%package -n libfsxfs-python3
Summary: Python 3 bindings for libfsxfs
Group: System Environment/Libraries
Requires: libfsxfs = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libfsxfs-python3
Python 3 bindings for libfsxfs

%package -n libfsxfs-tools
Summary: Several tools for reading X File System (XFS) volumes
Group: Applications/System
Requires: libfsxfs = %{version}-%{release} openssl 
BuildRequires: openssl-devel 

%description -n libfsxfs-tools
Several tools for reading X File System (XFS) volumes

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

%files -n libfsxfs
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libfsxfs-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libfsxfs-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfsxfs.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfsxfs-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libfsxfs-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libfsxfs-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Nov 17 2020 Joachim Metz <joachim.metz@gmail.com> 20201117-1
- Auto-generated

