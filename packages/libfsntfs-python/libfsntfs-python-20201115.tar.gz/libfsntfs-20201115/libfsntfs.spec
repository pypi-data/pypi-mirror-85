Name: libfsntfs
Version: 20201115
Release: 1
Summary: Library to access the Windows New Technology File System (NTFS) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfsntfs
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
               
BuildRequires: gcc               

%description -n libfsntfs
Library to access the Windows New Technology File System (NTFS) format

%package -n libfsntfs-static
Summary: Library to access the Windows New Technology File System (NTFS) format
Group: Development/Libraries
Requires: libfsntfs = %{version}-%{release}

%description -n libfsntfs-static
Static library version of libfsntfs.

%package -n libfsntfs-devel
Summary: Header files and libraries for developing applications for libfsntfs
Group: Development/Libraries
Requires: libfsntfs = %{version}-%{release}

%description -n libfsntfs-devel
Header files and libraries for developing applications for libfsntfs.

%package -n libfsntfs-python2
Obsoletes: libfsntfs-python < %{version}
Provides: libfsntfs-python = %{version}
Summary: Python 2 bindings for libfsntfs
Group: System Environment/Libraries
Requires: libfsntfs = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libfsntfs-python2
Python 2 bindings for libfsntfs

%package -n libfsntfs-python3
Summary: Python 3 bindings for libfsntfs
Group: System Environment/Libraries
Requires: libfsntfs = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libfsntfs-python3
Python 3 bindings for libfsntfs

%package -n libfsntfs-tools
Summary: Several tools for reading Windows New Technology File System (NTFS) volumes
Group: Applications/System
Requires: libfsntfs = %{version}-%{release} fuse-libs 
BuildRequires: fuse-devel 

%description -n libfsntfs-tools
Several tools for reading Windows New Technology File System (NTFS) volumes

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

%files -n libfsntfs
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libfsntfs-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libfsntfs-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfsntfs.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfsntfs-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libfsntfs-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libfsntfs-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Nov 15 2020 Joachim Metz <joachim.metz@gmail.com> 20201115-1
- Auto-generated

