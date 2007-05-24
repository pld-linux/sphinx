#  TODO
# - packages for Python/Ruby API
#
# Conditional build:
%bcond_without	pgsql		# without pgsql support
#
Summary:	Free open-source SQL full-text search engine
Summary(pl.UTF-8):	Silnik przeszukiwania pełnotekstowego SQL open-source
Name:		sphinx
Version:	0.9.7
Release:	0.4
License:	GPL v2
Group:		Applications/Databases
Source0:	http://www.sphinxsearch.com/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	32f2b7e98d8485c86108851d52c5cef4
Patch0:		%{name}-DESTDIR.patch
Source1:	sphinx.init
URL:		http://www.sphinxsearch.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mysql-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
Requires:	mysql-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sphinx is a a standalone search engine, meant to provide fast,
size-efficient and relevant fulltext search functions to other
applications. Sphinx was specially designed to integrate well with SQL
databases and scripting languages. Currently built-in data sources
support fetching data either via direct connection to MySQL, or from
an XML pipe.

%description -l pl.UTF-8
Sphinx jest samodzielnym silnikiem przeszukującym, dostarczającym
innym aplikacjom szybkie, zoptymalizowane rozmiarowo funkcje
przeszukiwania pełnotekstowego. Sphinx został specjalnie
zaprojektowany z myślą o dobrej integracji z bazami danych SQL oraz
językami skryptowymi. Obecnie wbudowane źródła danych wspierają
pobieranie danych poprzez bezpośrednie połączenie z MySQL lub z potoku
XML.

%package -n php-sphinx
Summary:	PHP API for Sphinx
Group:		Libraries
Requires:	php-common >= 4:5.0.4

%description -n php-sphinx
PHP API for Sphinx.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS=-D_FILE_OFFSET_BITS=64
%configure \
	%{?with_pgsql:--with-pgsql} \
	--with-mysql
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d,%{_datadir}/php}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/example.sql
mv $RPM_BUILD_ROOT%{_sysconfdir}/sphinx.conf{.dist,}
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/searchd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

cp -a api/sphinxapi.php $RPM_BUILD_ROOT%{_datadir}/php

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/sphinx.txt example.sql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sphinx.conf
%attr(755,root,root) %{_bindir}/indexer
%attr(755,root,root) %{_bindir}/search
%attr(755,root,root) %{_sbindir}/searchd
%attr(754,root,root) /etc/rc.d/init.d/%{name}

%files -n php-sphinx
%{_datadir}/php/sphinxapi.php
