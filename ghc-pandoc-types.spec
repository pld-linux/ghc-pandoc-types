#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	pandoc-types
Summary:	Types for representing a structured document
Summary(pl.UTF-8):	Typy do reprezentowania dokumentu posiadającego strukturę
Name:		ghc-%{pkgname}
Version:	1.20
Release:	2
License:	GPL v2+
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/pandoc-types
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	3bd9ed959e53bc4f2d2457098db584f2
Patch0:		QuickCheck-2.14.patch
URL:		http://hackage.haskell.org/package/pandoc-types
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-QuickCheck
BuildRequires:	ghc-aeson >= 0.6.2
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-containers >= 0.3
BuildRequires:	ghc-ghc-prim >= 0.2
BuildRequires:	ghc-syb >= 0.1
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-QuickCheck-prof
BuildRequires:	ghc-aeson-prof >= 0.6.2
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-containers-prof >= 0.3
BuildRequires:	ghc-ghc-prim-prof >= 0.2
BuildRequires:	ghc-syb-prof >= 0.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-QuickCheck
Requires:	ghc-aeson >= 0.6.2
Requires:	ghc-base >= 4
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-containers >= 0.3
Requires:	ghc-ghc-prim >= 0.2
Requires:	ghc-syb >= 0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Text.Pandoc.Definition defines the Pandoc data structure, which is
used by pandoc to represent structured documents. This module used to
live in the pandoc package, but starting with pandoc 1.7, it has been
split off, so that other packages can use it without drawing in all of
pandoc's dependencies, and pandoc itself can depend on packages (like
citeproc-hs) that use them.

Text.Pandoc.Builder provides functions for building up Pandoc
structures programmatically.

Text.Pandoc.Generic provides generic functions for manipulating Pandoc
documents.

Text.Pandoc.Walk provides faster, nongeneric functions for
manipulating Pandoc documents.

Text.Pandoc.JSON provides functions for serializing and deserializing
a Pandoc structure to and from JSON.

%description -l pl.UTF-8
Text.Pandoc.Definition definiuje strukturę danych Pandoc, służącą
programowi pandoc do reprezentowania dokumentów ze strukturą. Moduł
ten był wcześniej częścią pakietu pandoc, ale od wersji 1.7 został
wydzielony, dzięki czemu mogą z niego korzystać inne pakiety bez
pociągania wszystkich zależności pandoca, a pandoc może wymagać
pakietów używających tego modułu (np. citeproc-hs).

Text.Pandoc.Builder zapewnia funkcje do programowego budowania
struktur Pandoc.

Text.Pandoc.Generic udostępnia ogólne funkcje do operowania na
dokumentach Pandoc.

Text.Pandoc.Walk zapewnia szybkie, specyficzne funkcje do operowania
na dokumentach Pandoc.

Text.Pandoc.JSON zapewnia funkcje do serializacji i deserializacji
struktury Pandoc do/z formatu JSON.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-QuickCheck-prof
Requires:	ghc-aeson-prof >= 0.6.2
Requires:	ghc-base-prof >= 4
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-containers-prof >= 0.3
Requires:	ghc-ghc-prim-prof >= 0.2
Requires:	ghc-syb-prof >= 0.1

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpandoc-types-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpandoc-types-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpandoc-types-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Pandoc
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Pandoc/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Pandoc/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Pandoc/Legacy
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Pandoc/Legacy/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Pandoc/Legacy/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpandoc-types-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Pandoc/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Pandoc/Legacy/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
