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

%define		php_min_version 5.0.4
%include	/usr/lib/rpm/macros.php
%{?with_java:%include	/usr/lib/rpm/macros.java}
Summary:	Free open-source SQL full-text search engine
Summary(pl.UTF-8):	Silnik przeszukiwania pełnotekstowego SQL open-source
Name:		sphinx
Version:	2.2.11
Release:	2
License:	GPL v2, LGPL (API libraries)
Group:		Applications/Databases
Source0:	http://www.sphinxsearch.com/files/%{name}-%{version}-release.tar.gz
# Source0-md5:	5cac34f3d78a9d612ca4301abfcbd666
Source1:	%{name}.init
Source2:	%{name}.logrotate
Source3:	%{name}.conf.sh
Source4:	%{name}.tmpfiles
Patch0:		bug-468.patch
Patch1:		libstemmer.patch
Patch2:		x32.patch
URL:		http://www.sphinxsearch.com/
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.12
BuildRequires:	expat-devel
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libstdc++-devel
%{?with_libstemmer:BuildRequires:	libstemmer-devel}
BuildRequires:	libtool
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	python
BuildRequires:	python-modules
%{?with_java:BuildRequires:	rpm-javaprov}
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.647
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(sphinx)
Provides:	user(sphinx)
Conflicts:	logrotate < 3.8.0
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

%description -n libsphinxclient -l pl.UTF-8
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

%package -n java-sphinxapi
Summary:	Java API for Sphinx
Summary(pl.UTF-8):	API Javy dla Sphinksa
License:	LGPL
Group:		Development/Languages/Java
Requires:	jpackage-utils
Obsoletes:	java-sphinx < 2.0.3-5
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n java-sphinxapi
Java API for Sphinx.

%description -n java-sphinxapi -l pl.UTF-8
API Javy dla Sphinksa.

%package -n php-sphinxapi
Summary:	PHP API for Sphinx Search
Summary(pl.UTF-8):	API PHP dla Sphinksa
License:	LGPL
Group:		Libraries
Requires:	php(core) >= %{php_min_version}
Provides:	php(sphinx)
Obsoletes:	php-sphinx < 2.0.3-5
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n php-sphinxapi
PHP API for Sphinx Search.

%description -n php-sphinxapi -l pl.UTF-8
API PHP dla Sphinksa.

%package -n python-sphinxapi
Summary:	Python API for Sphinx Search
Summary(pl.UTF-8):	API Python dla Sphinksa
License:	LGPL
Group:		Development/Languages/Python
Requires:	python
Obsoletes:	python-sphinx < 2.0.3-5
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n python-sphinxapi
Python API for Sphinx Search.

%description -n python-sphinxapi -l pl.UTF-8
API Pythona dla Sphinksa.

%prep
%setup -q -n %{name}-%{version}-release
%patch0 -p1
#patch1 -p1
%patch2 -p1

sed -i -e '
	s#/var/run/#/var/run/sphinx/#
	s#@CONFDIR@/log/searchd.pid#/var/run/sphinx/searchd.pid#
	s#@CONFDIR@/log/#/var/log/sphinx/#g
	s#@CONFDIR@/data/#/var/lib/sphinx/#g
' sphinx*.conf.in

sed -i -e '
	s#libdirs="/usr/lib/x86_64-linux-gnu /usr/lib64 /usr/local/lib64 /usr/lib/i386-linux-gnu /usr/lib /usr/local/lib"#libdirs="/usr/libx32 /usr/lib64 /usr/lib"#
' configure

%build
CPPFLAGS=-D_FILE_OFFSET_BITS=64
%configure \
	--with%{!?with_libstemmer:out}-libstemmer \
	--with%{!?with_pgsql:out}-pgsql \
	--with%{!?with_mysql:out}-mysql \
	--with-syslog
%{__make} -j1
# use .conf ext for %doc
cp -pf sphinx.conf.dist sphinx.conf
cp -pf sphinx-min.conf.dist sphinx-min.conf

# libsphinxclient
cd api/libsphinxclient
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
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/{logrotate.d,rc.d/init.d}}\
	$RPM_BUILD_ROOT{/var/{log,run,lib}/%{name},/var/log/archive/%{name}} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_sysconfdir}/example.sql
rm $RPM_BUILD_ROOT%{_sysconfdir}/sphinx.conf.dist

# create default config with no index definition
sed -e '/## data source definition/,/## indexer settings/d' sphinx.conf > $RPM_BUILD_ROOT%{_sysconfdir}/sphinx-common.conf
# dir for indexes definition
install -d $RPM_BUILD_ROOT%{_sysconfdir}/index.d

rm $RPM_BUILD_ROOT%{_sysconfdir}/sphinx-min.conf.dist
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/searchd
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

install -d $RPM_BUILD_ROOT%{php_data_dir}
cp -p api/sphinxapi.php $RPM_BUILD_ROOT%{php_data_dir}

# libsphinxclient
%{__make} -C api/libsphinxclient install \
	DESTDIR=$RPM_BUILD_ROOT

# python api
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}
cp -p api/sphinxapi.py $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

# ruby api

# java api
%if %{with java}
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p api/java/sphinxapi.jar $RPM_BUILD_ROOT%{_javadir}/sphinxapi-%{version}.jar
ln -s sphinxapi-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/sphinxapi.jar
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

%triggerpostun -- %{name} < 0.9.9-7.6
if [ -f %{_sysconfdir}/sphinx.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/sphinx-common.conf{,.rpmnew}
	mv -f %{_sysconfdir}/sphinx.conf.rpmsave %{_sysconfdir}/sphinx-common.conf
	%service -q sphinx restart
fi

%files
%defattr(644,root,root,755)
%doc doc/sphinx.txt example.sql sphinx.conf sphinx-min.conf

%dir %attr(750,root,sphinx) %{_sysconfdir}
# main sphinx config
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,sphinx) %{_sysconfdir}/sphinx-common.conf
# shell wrapper which loads main config and extra indexes config
%attr(755,root,sphinx) %{_sysconfdir}/sphinx.conf
# put here *.conf files defining extra indexes
%dir %attr(750,root,sphinx) %{_sysconfdir}/index.d

%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/indexer
%attr(755,root,root) %{_bindir}/indextool
%attr(755,root,root) %{_bindir}/spelldump
%attr(755,root,root) %{_bindir}/wordbreaker
%attr(755,root,root) %{_sbindir}/searchd

%{_mandir}/man1/indexer.1*
%{_mandir}/man1/indextool.1*
%{_mandir}/man1/searchd.1*
%{_mandir}/man1/spelldump.1*
%{systemdtmpfilesdir}/%{name}.conf
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
%{_includedir}/sphinxclient.h

%files -n libsphinxclient-static
%defattr(644,root,root,755)
%{_libdir}/libsphinxclient.a

%if %{with java}
%files -n java-sphinxapi
%defattr(644,root,root,755)
%doc api/java/README
%{_javadir}/sphinx*.jar
%endif

%files -n php-sphinxapi
%defattr(644,root,root,755)
%{php_data_dir}/sphinxapi.php

%files -n python-sphinxapi
%defattr(644,root,root,755)
%{py_sitescriptdir}/*.py[co]
