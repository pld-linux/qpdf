#
# Conditional build:
%bcond_without	gnutls		# gnutls crypto provider
%bcond_with	openssl		# openssl crypto provider
%bcond_without	static_libs	# static library build
#
Summary:	Command-line tools and library for transforming PDF files
Summary(pl.UTF-8):	Narzędzia linii poleceń i biblioteka do przekształcania plików PDF
Name:		qpdf
Version:	11.5.0
Release:	0.1
# MIT: e.g. libqpdf/sha2.c
License:	Artistic v2.0, some parts MIT
Group:		Applications/Publishing
Source0:	https://downloads.sourceforge.net/qpdf/%{name}-%{version}.tar.gz
# Source0-md5:	d916ac26b7f30a5cf3827c708c455ec9
URL:		https://qpdf.sourceforge.net/
BuildRequires:	cmake
# sha256sum
BuildRequires:	coreutils >= 6.3
%{?with_gnutls:BuildRequires:	gnutls-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libtool >= 2:2
BuildRequires:	make >= 3.81
%{?with_openssl:BuildRequires:	openssl-devel >= 1.1.0}
BuildRequires:	perl-Digest-MD5
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QPDF is a command-line program that does structural,
content-preserving transformations on PDF files. It could have been
called something like pdf-to-pdf. It includes support for merging and
splitting PDFs and to manipulate the list of pages in a PDF file. It
is not a PDF viewer or a program capable of converting PDF into other
formats.

%description -l pl.UTF-8
QPDF to działający z linii poleceń program wykonujący strukturalne,
zachowujące treść przekształcenia plików PDF. Można by go nazwać czymś
w rodzaju pdf-to-pdf. Zawiera obsługę łączenia i dzielenia PDF-ów oraz
operacji na liście stron w pliku PDF. Nie jest to przeglądarka plików
PDF ani konwerter PDF-ów do innych formatów.

%package libs
Summary:	QPDF library for transforming PDF files
Summary(pl.UTF-8):	Biblioteka QPDF do przekształcania plików PDF
Group:		Libraries

%description libs
QPDF is a C++ library that inspect and manipulate the structure of PDF
files. It can encrypt and linearize files, expose the internals of a
PDF file, and do many other operations useful to PDF developers.

%description libs -l pl.UTF-8
QPDF to biblioteka C++ analizująca i operująca na strukturze plików
PDF. Potrafi szyfrować i linearyzować pliki, udostępniać wnętrzności
plików PDF oraz wykonywać inne operacje przydatne programistom PDF.

%package devel
Summary:	Development files for QPDF library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki QPDF
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libjpeg-devel
Requires:	libstdc++-devel >= 6:5
Requires:	zlib-devel

%description devel
Header files necessary for developing programs using the QPDF library.

%description devel -l pl.UTF-8
Pliki nagłówkowe niezbędne do tworzenia programów wykorzystujących
bibliotekę QPDF.

%package static
Summary:	Static QPDF library
Summary(pl.UTF-8):	Statyczna biblioteka QPDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static QPDF library.

%description static -l pl.UTF-8
Statyczna biblioteka QPDF.

%prep
%setup -q

%build
mkdir build
cd build
%cmake \
	-DUSE_IMPLICIT_CRYPTO=OFF \
	-DREQUIRE_CRYPTO_NATIVE=ON \
	%{!?with_static_libs:-DBUILD_STATIC_LIBS=OFF} \
	%{?with_gnutls:-DREQUIRE_CRYPTO_GNUTLS=ON} \
	%{?with_openssl:-DREQUIRE_CRYPTO_OPENSSL=ON} \
	-DSHOW_FAILED_TEST_OUTPUT=ON \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name}-%{version} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	..

# SHELL= is workaround for some build failures
%{__make} \
	SHELL=/bin/sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cd build
%{__make} install \
	SHELL=/bin/sh \
	DESTDIR=$RPM_BUILD_ROOT
cd ..
cp -a examples/*.c* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README.md TODO.md
%attr(755,root,root) %{_bindir}/fix-qdf
%attr(755,root,root) %{_bindir}/qpdf
%attr(755,root,root) %{_bindir}/zlib-flate
%{_mandir}/man1/fix-qdf.1*
%{_mandir}/man1/qpdf.1*
%{_mandir}/man1/zlib-flate.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqpdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqpdf.so.29

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqpdf.so
%{_includedir}/qpdf
%{_pkgconfigdir}/libqpdf.pc
%{_examplesdir}/%{name}-%{version}
%{_libdir}/cmake/qpdf/libqpdfTargets-relwithdebinfo.cmake
%{_libdir}/cmake/qpdf/libqpdfTargets.cmake
%{_libdir}/cmake/qpdf/qpdfConfig.cmake
%{_libdir}/cmake/qpdf/qpdfConfigVersion.cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libqpdf.a
%endif
