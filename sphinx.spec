#
# TODO:
#  - package for ruby API
#
# Conditional build:
%bcond_without	java		# without Java support
%bcond_without	libstemmer	# without libstemmer support
%bcond_without	mysql		# without MySQL support
%bcond_without	pgsql		# without PostgreSQL support

# arch list synced with java-sun
%ifnarch i586 i686 pentium3 pentium4 athlon %{x8664}
%undefine	with_java
%endif

%{?with_java:%include	/usr/lib/rpm/macros.java}
%include	/usr/lib/rpm/macros.php
%define		php_min_version 5.0.4
Summary:	Free open-source SQL full-text search engine
Summary(pl.UTF-8):	Silnik przeszukiwania pełnotekstowego SQL open-source
Name:		sphinx
Version:	0.9.8.1
Release:	2
License:	GPL v2
Group:		Applications/Databases
Source0:	http://www.sphinxsearch.com/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	428a14df41fb425e664d9e2d6178c037
Source1:	%{name}.init
Patch0:		%{name}-system-libstemmer.patch
URL:		http://www.sphinxsearch.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
%{?with_java:BuildRequires:	java-sun}
BuildRequires:	libstdc++-devel
%{?with_libstemmer:BuildRequires:	libstemmer-devel}
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpm-javaprov
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.461
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

%package -n libsphinxclient
Summary:	Client library for Sphinx
Summary(pl.UTF-8):	Biblioteka kliencka do Sphinx
Group:		Libraries

%description -n libsphinxclient
This package provides a client library for Sphinx search engine.

%description -n libsphinxclient -l PL.UTF_8
Ten pakiet dostarcza bibliotekę kliencką do silnika Sphinx.

%package -n libsphinxclient-devel
Summary:	Header files for sphinxclient library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sphinxclient
Group:		Development/Libraries
Requires:	libsphinxclient = %{version}-%{release}

%description -n libsphinxclient-devel
Header files for sphinxclient library.

%description -n libsphinxclient-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sphinxclient.

%package -n libsphinxclient-static
Summary:	Static sphinxclient library
Summary(pl.UTF-8):	Statyczna biblioteka sphinxclient
Group:		Development/Libraries
Requires:	libsphinxclient-devel = %{version}-%{release}

%description -n libsphinxclient-static
Static sphinxclient library.

%description -n libsphinxclient-static -l pl.UTF-8
Statyczna biblioteka sphinxclient.

%package -n java-sphinx
Summary:	Java API for Sphinx
Summary(pl.UTF-8):	API Javy dla Sphinksa
Group:		Development/Languages/Java
Requires:	jpackage-utils

%description -n java-sphinx
Java API for Sphinx.

%description -n java-sphinx -l pl.UTF-8
API Javy dla Sphinksa.

%package -n php-sphinx
Summary:	PHP API for Sphinx
Summary(pl.UTF-8):	API PHP dla Sphinksa
Group:		Libraries
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-mbstring

%description -n php-sphinx
PHP API for Sphinx.

%description -n php-sphinx -l pl.UTF-8
API PHP dla Sphinksa.

%package -n python-sphinx
Summary:	Python API for Sphinx
Summary(pl.UTF-8):	API Python dla Sphinksa
Group:		Development/Languages/Python
%pyrequires_eq	python

%description -n python-sphinx
Python API for Sphinx.

%description -n python-sphinx -l pl.UTF-8
API Pythona dla Sphinksa.

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
	--with%{!?with_libstemmer:out}-libstemmer \
	--with%{!?with_pgsql:out}-pgsql \
	--with%{!?with_mysql:out}-mysql
%{__make} -j1

# libsphinxclient
cd api/libsphinxclient
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS=-D_FILE_OFFSET_BITS=64
%configure
%{__make} -j1
cd ../..

# java api
%if %{with java}
export JAVA_HOME="%{java_home}"
%{__make} -j1 -C api/java
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/example.sql
mv $RPM_BUILD_ROOT%{_sysconfdir}/sphinx.conf{.dist,}
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/searchd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

install -d $RPM_BUILD_ROOT%{php_data_dir}
cp -a api/sphinxapi.php $RPM_BUILD_ROOT%{php_data_dir}

# libsphinxclient
%{__make} -C api/libsphinxclient install \
	DESTDIR=$RPM_BUILD_ROOT

# python api
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}
install api/sphinxapi.py $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

# ruby api

# java api
%if %{with java}
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a api/java/sphinxapi.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libsphinxclient -p /sbin/ldconfig
%postun	-n libsphinxclient -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/sphinx.txt example.sql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sphinx.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sphinx-min.conf.dist
%attr(755,root,root) %{_bindir}/indexer
%attr(755,root,root) %{_bindir}/search
%attr(755,root,root) %{_bindir}/spelldump
%attr(755,root,root) %{_sbindir}/searchd
%attr(754,root,root) /etc/rc.d/init.d/%{name}

%files -n libsphinxclient
%defattr(644,root,root,755)
%doc api/libsphinxclient/README
%attr(755,root,root) %{_libdir}/libsphinxclient-*.*.*.so

%files -n libsphinxclient-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsphinxclient.so
%{_libdir}/libsphinxclient.la
%{_includedir}/*.h

%files -n libsphinxclient-static
%defattr(644,root,root,755)
%{_libdir}/libsphinxclient.a

%if %{with java}
%files -n java-sphinx
%defattr(644,root,root,755)
%doc api/java/README
%{_javadir}/sphinx*.jar
%endif

%files -n php-sphinx
%defattr(644,root,root,755)
%{php_data_dir}/sphinxapi.php

%files -n python-sphinx
%defattr(644,root,root,755)
%{py_sitescriptdir}/*.py?
