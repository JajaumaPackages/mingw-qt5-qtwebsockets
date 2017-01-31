%?mingw_package_header

%global qt_module qtwebsockets
#%%global pre rc1

#%%global snapshot_date 20130510
#%%global snapshot_rev 8d6a8446

%if 0%{?snapshot_date}
%global source_folder qt-%{qt_module}
%else
%global source_folder %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
%endif

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-qt5-%{qt_module}
Version:        5.6.0
Release:        1%{?pre:.%{pre}}%{?snapshot_date:.git%{snapshot_date}.%{snapshot_rev}}%{?dist}
Summary:        Qt5 for Windows - QtWebsockets component

License:        GPLv3 with exceptions or LGPLv2 with exceptions
Group:          Development/Libraries
URL:            http://www.qtsoftware.com/

%if 0%{?snapshot_date}
# To regenerate:
# wget http://qt.gitorious.org/qt/%{qt_module}/archive-tarball/%{snapshot_rev} -O qt5-%{qt_module}-%{snapshot_rev}.tar.gz
Source0:        qt5-%{qt_module}-%{snapshot_rev}.tar.gz
%else
%if "%{?pre}" != ""
Source0:        http://download.qt-project.org/development_releases/qt/%{release_version}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0:        http://download.qt-project.org/official_releases/qt/%{release_version}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 96
BuildRequires:  mingw32-qt5-qtbase >= 5.6.0
BuildRequires:  mingw32-qt5-qtdeclarative >= 5.6.0

BuildRequires:  mingw64-filesystem >= 96
BuildRequires:  mingw64-qt5-qtbase >= 5.6.0
BuildRequires:  mingw64-qt5-qtdeclarative >= 5.6.0


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtWebsockets component

%description -n mingw32-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win64
%package -n mingw64-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtWebsockets component

%description -n mingw64-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%?mingw_debug_package


%prep
%setup -q -n %{source_folder}

%if 0%{?snapshot_date}
# Make sure the syncqt tool is run because we're using a git snapshot
# Otherwise the build fails against Qt 5.1
mkdir .git
%endif


%build
%mingw_qmake_qt5 ../%{qt_module}.pro
%mingw_make %{?_smp_mflags}


%install
%mingw_make install INSTALL_ROOT=$RPM_BUILD_ROOT

# .prl files aren't interesting for us
find $RPM_BUILD_ROOT -name "*.prl" -delete

# Create a list of .dll.debug files which need to be excluded from the main packages
# We do this to keep the %%files section as clean/readable as possible (otherwise every
# single file and directory would have to be mentioned individually in the %%files section)
# Note: the .dll.debug files aren't created yet at this point (as it happens after
# the %%install section). Therefore we have to assume that all .dll files will
# eventually get a .dll.debug counterpart
find $RPM_BUILD_ROOT%{mingw32_prefix} | grep .dll | grep -v .dll.a | sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw32-qt5-%{qt_module}.excludes
find $RPM_BUILD_ROOT%{mingw64_prefix} | grep .dll | grep -v .dll.a | sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw64-qt5-%{qt_module}.excludes


# Win32
%files -n mingw32-qt5-%{qt_module} -f mingw32-qt5-%{qt_module}.excludes
%doc LGPL_EXCEPTION.txt LICENSE.LGPLv21 LICENSE.LGPLv3 README.md
%{mingw32_bindir}/Qt5WebSockets.dll
%{mingw32_includedir}/qt5/QtWebSockets/
%{mingw32_libdir}/cmake/Qt5WebSockets/
%{mingw32_libdir}/libQt5WebSockets.dll.a
%{mingw32_libdir}/pkgconfig/Qt5WebSockets.pc
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_websockets.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_websockets_private.pri
%{mingw32_datadir}/qt5/qml/Qt/WebSockets/
%{mingw32_datadir}/qt5/qml/QtWebSockets/

# Win64
%files -n mingw64-qt5-%{qt_module} -f mingw64-qt5-%{qt_module}.excludes
%doc LGPL_EXCEPTION.txt LICENSE.LGPLv21 LICENSE.LGPLv3 README.md
%{mingw64_bindir}/Qt5WebSockets.dll
%{mingw64_includedir}/qt5/QtWebSockets/
%{mingw64_libdir}/cmake/Qt5WebSockets/
%{mingw64_libdir}/libQt5WebSockets.dll.a
%{mingw64_libdir}/pkgconfig/Qt5WebSockets.pc
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_websockets.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_websockets_private.pri
%{mingw64_datadir}/qt5/qml/Qt/WebSockets/
%{mingw64_datadir}/qt5/qml/QtWebSockets/


%changelog
* Sun Apr 10 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-1
- Update to 5.6.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-1
- Update to 5.5.1

* Sat Aug  8 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 11 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-2
- Rebuild against latest mingw-gcc

* Tue Mar 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-1
- Update to 5.4.1

* Thu Jan  1 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-1
- Initial release

