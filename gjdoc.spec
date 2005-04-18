Summary:	Documentation generation framework for Java source files
Name:		gjdoc
Version:	0.7.3
Release:	1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	639b8b82cc2a5f79415052daf9d367f3
URL:		http://www.gnu.org/software/classpath/cp-tools/
BuildRequires:	antlr >= 2.7.5-3
# Some versions of gcj are known to produce bad bytecode.
# At least bug 19921 is known to affect gjdoc (in Feb 2005).
BuildRequires:	gcc-java >= 5:4.0.0-0.20050416.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gjdoc is a documentation framework for generating documentation in
various formats from java source file. It is both a drop-in
replacement for the traditional command line tool `javadoc' and
provides an interface for inspection of and generation of different
output for java source packages, classes, methods and fields.

Gjdoc's current version implements all features of the traditional
javadoc tool up to version 1.4. With the exception of two
unimplemented options (-nocomment and -serialwarn) it should be fully
command-line compatible, and it provides a compatible Doclet API
(com.sun.javadoc).

However, in contrast to Javadoc, `gjdoc' does not perfom syntax
checking on the supplied sources. If necessary, use a real compiler
like `gcj -fsyntax-only` or `jikes +B' for checking the sources
beforehand.

%prep
%setup -q

%build
%configure \
	--enable-shared \
	--disable-static \
	--enable-native

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
%ldconfig_post

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
%ldconfig_postun

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gjdoc
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_infodir}/gjdoc.*
%{_javadir}/*.jar
%{_mandir}/man1/gjdoc.1*
