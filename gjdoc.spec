#
# Conditional build:
%bcond_with	native	# build native library
#
Summary:	Documentation generation framework for Java source files
Summary(pl.UTF-8):	Szkielet do generowania dokumentacji dla plików źródłowych w Javie
Name:		gjdoc
Version:	0.7.8
Release:	1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	a60c6bb229025120412b8a9d69ef1800
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/classpath/cp-tools/
BuildRequires:	antlr >= 2.7.5-3
# Some versions of gcj are known to produce bad bytecode.
# At least bug 19921 is known to affect gjdoc (in Feb 2005).
BuildRequires:	gcc-java >= 5:4.0.0-0.20050416.1
BuildRequires:	texinfo
Requires:	jpackage-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gjdoc is a documentation framework for generating documentation in
various formats from Java source files. It is both a drop-in
replacement for the traditional command line tool `javadoc' and
provides an interface for inspection of and generation of different
output for Java source packages, classes, methods and fields.

Gjdoc's current version implements all features of the traditional
javadoc tool up to version 1.4. With the exception of two
unimplemented options (-nocomment and -serialwarn) it should be fully
command-line compatible, and it provides a compatible Doclet API
(com.sun.javadoc).

However, in contrast to Javadoc, `gjdoc' does not perfom syntax
checking on the supplied sources. If necessary, use a real compiler
like `gcj -fsyntax-only` or `jikes +B' for checking the sources
beforehand.

%description -l pl.UTF-8
gjdoc to szkielet służący do generowania dokumentacji w różnych
formatach z plików źródłowych w Javie. Jest to zarówno zamiennik
tradycyjnego polecenia javadoc, jak i interfejs do inspekcji i
generowania różnych formatów wyjściowych dla pakietów źródłowych,
klas, metod i pól w Javie.

Aktualna wersja gjdoc implementuje wszystkie możliwości tradycyjnego
narzędzia javadoc do wersji 1.4. Z wyjątkiem dwóch nieudokumentowanych
opcji (-nocomment i -serialwarn) powinna być w pełni zgodna co do
linii poleceń i dostarcza kompatybilne Doclet API (com.sun.javadoc).

Jednak, w porównaniu do Javadoc, gjdoc nie sprawdza składni źródeł. W
razie potrzeby źródła można sprawdzić przedtem prawdziwym
kompilatorem, np. "gcj -fsyntax-only" lub "jikes +B".

%prep
%setup -q
%patch0 -p1

%build
%configure \
	GCJFLAGS="%{rpmcflags}" \
	--with-antlr-jar=%{_javadir}/antlr.jar \
	--%{?with_native:en}%{!?with_native:dis}able-native \
	--enable-shared \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gjdoc
%if %{with native}
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%endif
%{_infodir}/gjdoc.info*
%{_javadir}/*.jar
%{_mandir}/man1/gjdoc.1*
