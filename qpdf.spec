Summary:	Command-line tools and library for transforming PDF files
Name:		qpdf
Version:	5.0.1
Release:	2
# MIT: e.g. libqpdf/sha2.c
License:	Artistic 2.0 and MIT
Group:		Applications/Publishing
Source0:	http://downloads.sourceforge.net/qpdf/%{name}-%{version}.tar.gz
# Source0-md5:	6efd89c18461cb73f77bb60cb2da4bce
URL:		http://qpdf.sourceforge.net/
BuildRequires:	pcre-devel
BuildRequires:	perl
BuildRequires:	perl(Digest::MD5)
BuildRequires:	zlib-devel
Requires:	qpdf-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QPDF is a command-line program that does structural,
content-preserving transformations on PDF files. It could have been
called something like pdf-to-pdf. It includes support for merging and
splitting PDFs and to manipulate the list of pages in a PDF file. It
is not a PDF viewer or a program capable of converting PDF into other
formats.

%package libs
Summary:	QPDF library for transforming PDF files
Group:		Libraries

%description libs
QPDF is a C++ library that inspect and manipulate the structure of PDF
files. It can encrypt and linearize files, expose the internals of a
PDF file, and do many other operations useful to PDF developers.

%package devel
Summary:	Development files for QPDF library
Group:		Development/Libraries
Requires:	qpdf-libs = %{version}-%{release}

%description devel
Header files and libraries necessary for developing programs using the
QPDF library.

%prep
%setup -q

%{__sed} -i -e '1s,^#!/usr/bin/env perl,#!/usr/bin/perl,' qpdf/fix-qdf

%build
%configure \
	--docdir=%{_docdir}/%{name}-%{version} \
	--disable-static \
	--enable-show-failed-test-output

%{__make} SHELL=/bin/sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	SHELL=/bin/sh \
	DESTDIR=$RPM_BUILD_ROOT

cp -a examples/*.c* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libqpdf.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*.{pdf,html,css}
%doc README TODO ChangeLog
%attr(755,root,root) %{_bindir}/fix-qdf
%attr(755,root,root) %{_bindir}/qpdf
%attr(755,root,root) %{_bindir}/zlib-flate
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqpdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqpdf.so.13

%files devel
%defattr(644,root,root,755)
%{_includedir}/qpdf
%attr(755,root,root) %{_libdir}/libqpdf.so
%{_pkgconfigdir}/libqpdf.pc
%{_examplesdir}/%{name}-%{version}
