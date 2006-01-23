Summary:	Documentation generation framework for Java source files
Summary(pl):	Szkielet do generowania dokumentacji dla plików ¼ród³owych w Javie
Name:		gjdoc
Version:	0.7.7
Release:	1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	f9755ee2601f7903360680694747a8c7
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/classpath/cp-tools/
BuildRequires:	antlr >= 2.7.5-3
# Some versions of gcj are known to produce bad bytecode.
# At least bug 19921 is known to affect gjdoc (in Feb 2005).
BuildRequires:	gcc-java >= 5:4.0.0-0.20050416.1
BuildRequires:	texinfo
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

%description -l pl
gjdoc to szkielet s³u¿±cy do generowania dokumentacji w ró¿nych
formatach z plików ¼ród³owych w Javie. Jest to zarówno zamiennik
tradycyjnego polecenia javadoc, jak i interfejs do inspekcji i
generowania ró¿nych formatów wyj¶ciowych dla pakietów ¼ród³owych,
klas, metod i pól w Javie.

Aktualna wersja gjdoc implementuje wszystkie mo¿liwo¶ci tradycyjnego
narzêdzia javadoc do wersji 1.4. Z wyj±tkiem dwóch nieudokumentowanych
opcji (-nocomment i -serialwarn) powinna byæ w pe³ni zgodna co do
linii poleceñ i dostarcza kompatybilne Doclet API (com.sun.javadoc).

Jednak, w porównaniu do Javadoc, gjdoc nie sprawdza sk³adni ¼róde³. W
razie potrzeby ¼ród³a mo¿na sprawdziæ przedtem prawdziwym
kompilatorem, np. "gcj -fsyntax-only" lub "jikes +B".

%prep
%setup -q
%patch0 -p1

%build
%configure \
	GCJFLAGS="%{rpmcflags}" \
	--with-antlr-jar=%{_javadir}/antlr.jar \
	--enable-native \
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
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/ldconfig

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gjdoc
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_infodir}/gjdoc.info*
%{_javadir}/*.jar
%{_mandir}/man1/gjdoc.1*
