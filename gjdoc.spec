#
# Conditional build:
%bcond_with	native	# build native library
#
Summary:	Documentation generation framework for Java source files
Summary(pl.UTF-8):	Szkielet do generowania dokumentacji dla plików źródłowych w Javie
Name:		gjdoc
Version:	0.7.9
Release:	3
License:	GPL v2+
Group:		Development/Languages/Java
Source0:	http://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	24cade2efe22d5adefcbabb21f094803
Patch0:		%{name}-info.patch
Patch1:		%{name}-launcher.patch
Patch2:		%{name}-link.patch
URL:		http://www.gnu.org/software/classpath/cp-tools/
BuildRequires:	antlr >= 2.7.5-3
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
# Some versions of gcj are known to produce bad bytecode.
# At least bug 19921 is known to affect gjdoc (in Feb 2005).
BuildRequires:	gcc-java >= 5:4.0.0-0.20050416.1
BuildRequires:	libtool >= 2:1.5
BuildRequires:	texinfo
Requires:	jpackage-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# circular dependency with lib-gnu-classpath-tools (void gnu::classpath::tools::gjdoc::Main::main(JArray<java::lang::String*>*))
%define		skip_post_check_so	lib-com-sun-javadoc.so.*

# some -W flags are not valid for Java, filter them out to avoid warnings (which break libtool configure)
%define		gcjflags	%(echo %{rpmcflags} | sed -e 's/ -Wformat[^ ]*//g')

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
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	GCJFLAGS="%{gcjflags}" \
	--with-antlr-jar=%{_javadir}/antlr.jar \
	--enable-native%{!?with_native:=no} \
	--enable-shared \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{lib-com-sun-javadoc,lib-com-sun-tools-doclets-Taglet,lib-gnu-classpath-tools-gjdoc}.{la,so}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{?with_native:/sbin/ldconfig}
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
%{?with_native:/sbin/ldconfig}
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gjdoc
%if %{with native}
%attr(755,root,root) %{_libdir}/lib-com-sun-javadoc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib-com-sun-javadoc.so.0
%attr(755,root,root) %{_libdir}/lib-com-sun-tools-doclets-Taglet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib-com-sun-tools-doclets-Taglet.so.0
%attr(755,root,root) %{_libdir}/lib-gnu-classpath-tools-gjdoc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib-gnu-classpath-tools-gjdoc.so.0
%endif
%{_infodir}/gjdoc.info*
%{_javadir}/com-sun-javadoc-%{version}.jar
%{_javadir}/com-sun-tools-doclets-Taglet-%{version}.jar
%{_javadir}/gnu-classpath-tools-gjdoc-%{version}.jar
%{_mandir}/man1/gjdoc.1*
