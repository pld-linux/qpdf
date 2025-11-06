#
# Conditional build:
%bcond_without	gnutls		# gnutls crypto provider
%bcond_with	openssl		# openssl crypto provider
%bcond_without	zopfli		# zopfli based compression support
%bcond_without	static_libs	# static library build
#
Summary:	Command-line tools and library for transforming PDF files
Summary(pl.UTF-8):	Narzędzia linii poleceń i biblioteka do przekształcania plików PDF
Name:		qpdf
Version:	12.2.0
Release:	1
# MIT: e.g. libqpdf/sha2.c
License:	Artistic v2.0, some parts MIT
Group:		Applications/Publishing
Source0:	https://downloads.sourceforge.net/qpdf/%{name}-%{version}.tar.gz
# Source0-md5:	f10f5b3a0635e9fd2f305880c5cd8534
URL:		https://qpdf.sourceforge.net/
BuildRequires:	cmake >= 3.16
# sha256sum
BuildRequires:	coreutils >= 6.3
%{?with_gnutls:BuildRequires:	gnutls-devel}
%ifnarch %arch_with_atomics64
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	make >= 1:3.81
%{?with_openssl:BuildRequires:	openssl-devel >= 1.1.0}
BuildRequires:	perl-Digest-MD5
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.047
BuildRequires:	zlib-devel
%{?with_zopfli:BuildRequires:	zopfli-devel}
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
Requires:	libstdc++-devel >= 6:7
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
%cmake -B build \
	%{!?with_static_libs:-DBUILD_STATIC_LIBS=OFF} \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name}-%{version} \
	%{?with_gnutls:-DREQUIRE_CRYPTO_GNUTLS=ON} \
	-DREQUIRE_CRYPTO_NATIVE=ON \
	%{?with_openssl:-DREQUIRE_CRYPTO_OPENSSL=ON} \
	-DSHOW_FAILED_TEST_OUTPUT=ON \
	-DUSE_IMPLICIT_CRYPTO=OFF \
	-DZOPFLI=%{__ON_OFF zopfli}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{bash_compdir},%{zsh_compdir}}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a examples/*.c* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a completions/bash/qpdf $RPM_BUILD_ROOT%{bash_compdir}
cp -a completions/zsh/_qpdf $RPM_BUILD_ROOT%{zsh_compdir}

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
%{bash_compdir}/qpdf
%{zsh_compdir}/_qpdf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqpdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqpdf.so.30

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqpdf.so
%{_includedir}/qpdf
%{_pkgconfigdir}/libqpdf.pc
%{_examplesdir}/%{name}-%{version}
%{_libdir}/cmake/qpdf

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libqpdf.a
%endif
