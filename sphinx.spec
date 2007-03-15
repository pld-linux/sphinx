%define		_rc		rc2
%define		_rel	0.2
Summary:	Free open-source SQL full-text search engine
Summary(pl.UTF-8):	Silnik przeszukiwania pełnotekstowego SQL open-source
Name:		sphinx
Version:	0.9.7
Release:	0.%{_rc}.%{_rel}
License:	GPL v2
Group:		Applications/Databases
Source0:	http://www.sphinxsearch.com/downloads/%{name}-%{version}-%{_rc}.tar.gz
# Source0-md5:	65daf0feb7e276fb3de0aba82cff1d3e
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.sphinxsearch.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mysql-devel
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
pobieranie danych poprzez bezpośrednie połączenie z MySQL lub
z potoku XML.

%prep
%setup -q -n %{name}-%{version}-%{_rc}
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS=-D_FILE_OFFSET_BITS=64
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/example.sql
mv $RPM_BUILD_ROOT%{_sysconfdir}/sphinx.conf{.dist,}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/sphinx.txt example.sql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sphinx.conf
%attr(755,root,root) %{_bindir}/indexer
%attr(755,root,root) %{_bindir}/search
%attr(755,root,root) %{_bindir}/searchd
