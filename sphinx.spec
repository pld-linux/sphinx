# TODO:
#  - package for ruby API
#  - subpackage for driver backend deps if code patched to support it:
#    sphinx-0.9.9-2.i686: required "libodbc.so.1" is provided by following packages:
#    libmysqlclient.so.16 libmysqlclient.so.16(libmysqlclient_16) libpq.so.5
#
# Conditional build:
%bcond_without	java		# without Java support
%bcond_without	libstemmer	# without libstemmer support
%bcond_without	mysql		# without MySQL support
%bcond_without	pgsql		# without PostgreSQL support

%undefine	with_java

%{?with_java:%include	/usr/lib/rpm/macros.java}
%include	/usr/lib/rpm/macros.php
%define		php_min_version 5.0.4
Summary:	Free open-source SQL full-text search engine
Summary(pl.UTF-8):	Silnik przeszukiwania pełnotekstowego SQL open-source
Name:		sphinx
Version:	0.9.9
Release:	3
License:	GPL v2
Group:		Applications/Databases
Source0:	http://www.sphinxsearch.com/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	7b9b618cb9b378f949bb1b91ddcc4f54
Source1:	%{name}.init
Source2:	%{name}.logrotate
Patch0:		%{name}-system-libstemmer.patch
Patch1:		bug-468.patch
URL:		http://www.sphinxsearch.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libstdc++-devel
%{?with_libstemmer:BuildRequires:	libstemmer-devel}
BuildRequires:	libtool
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	rpm-javaprov
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.461
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(sphinx)
Provides:	user(sphinx)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

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
%patch1 -p1

sed -i -e '
	s#/var/run/#/var/run/sphinx/#
	s#@CONFDIR@/log/searchd.pid#/var/run/sphinx/searchd.pid#
	s#@CONFDIR@/log/#/var/log/sphinx/#g
	s#@CONFDIR@/data/#/var/lib/sphinx/#g
' sphinx*.conf.in

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
# use .conf ext for %doc
cp -f sphinx.conf.dist sphinx.conf
cp -f sphinx-min.conf.dist sphinx-min.conf

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
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/{logrotate.d,rc.d/init.d},/var/{log,run,lib}/%{name},/var/log/archive/%{name}}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_sysconfdir}/example.sql
rm $RPM_BUILD_ROOT%{_sysconfdir}/sphinx.conf.dist

# create default config with no index definition
sed -e '/## data source definition/,/## indexer settings/d' sphinx.conf > $RPM_BUILD_ROOT%{_sysconfdir}/sphinx.conf

rm $RPM_BUILD_ROOT%{_sysconfdir}/sphinx-min.conf.dist
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/searchd
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

install -d $RPM_BUILD_ROOT%{php_data_dir}
cp -a api/sphinxapi.php $RPM_BUILD_ROOT%{php_data_dir}

# libsphinxclient
%{__make} -C api/libsphinxclient install \
	DESTDIR=$RPM_BUILD_ROOT

# python api
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}
cp -a api/sphinxapi.py $RPM_BUILD_ROOT%{py_sitescriptdir}
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

%pre
%groupadd -g 249 sphinx
%useradd -u 249 -d /var/lib/%{name} -g sphinx -c "Sphinx Search" sphinx

%post
/sbin/chkconfig --add sphinx
%service sphinx restart

%preun
if [ "$1" = 0 ]; then
	%service sphinx stop
	/sbin/chkconfig --del sphinx
fi

%files
%defattr(644,root,root,755)
%doc doc/sphinx.txt example.sql sphinx.conf sphinx-min.conf
%dir %attr(750,root,sphinx) %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,sphinx) %{_sysconfdir}/sphinx.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/indexer
%attr(755,root,root) %{_bindir}/indextool
%attr(755,root,root) %{_bindir}/search
%attr(755,root,root) %{_bindir}/spelldump
%attr(755,root,root) %{_sbindir}/searchd

%dir %attr(771,root,sphinx) /var/run/sphinx
%dir %attr(770,root,sphinx) /var/log/sphinx
%dir %attr(770,root,sphinx) /var/log/archive/sphinx
%dir %attr(770,root,sphinx) /var/lib/sphinx

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
%{py_sitescriptdir}/*.py[co]
