%{?scl:%scl_package mvel}
%{!?scl:%global pkg_name %{name}}

%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:          %{?scl_prefix}mvel
Version:       2.2.7
Release:       3%{?dist}
Summary:       MVFLEX Expression Language
License:       ASL 2.0
Url:           https://github.com/%{pkg_name}
Source0:       https://github.com/%{pkg_name}/%{pkg_name}/archive/%{pkg_name}2-%{namedversion}.tar.gz
Source1:       %{pkg_name}-script
# remove tests which require internal objectweb-asm libraries
Patch0:        %{pkg_name}-%{namedversion}-tests.patch
Patch1:        unbundle_asm.patch

BuildRequires: %{?scl_mvn_prefix}maven-local
BuildRequires: %{?scl_mvn_prefix}mvn(com.thoughtworks.xstream:xstream)
BuildRequires: %{?scl_java_prefix}junit
BuildRequires: %{?scl_mvn_prefix}maven-plugin-bundle
BuildRequires: %{?scl_mvn_prefix}mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: %{?scl_mvn_prefix}mvn(org.apache.maven.plugins:maven-surefire-report-plugin)
BuildRequires: %{?scl_java_prefix}objectweb-asm%{?scl:5}
%{?scl:Requires: %scl_runtime}

BuildArch:     noarch

%description
MVEL is a powerful expression language for Java-based applications. It
provides a plethora of features and is suited for everything from the
smallest property binding and extraction, to full blown scripts.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-%{pkg_name}2-%{namedversion}
find . -name "*.jar" -delete
find . -name "*.class" -delete

rm ASM-LICENSE.txt

%patch0 -p1

# See https://bugzilla.redhat.com/show_bug.cgi?id=1095339
sed -i '/Unsafe/d' src/main/java/org/mvel2/util/JITClassLoader.java

%{?scl_enable}
# Uwanted
%pom_remove_plugin :maven-source-plugin
# Remove org.apache.maven.wagon:wagon-webdav:1.0-beta-2
%pom_xpath_remove "pom:project/pom:build/pom:extensions"

# remove bundled asm
rm -rf src/main/java/org/mvel2/asm
# patch asm dependent files so that they depend on org.objectweb.asm
%patch1 -p1
# add asm dependency as the bundled one is removed
%pom_add_dep org.ow2.asm:asm:5
%pom_add_dep org.ow2.asm:asm-util:5

sed -i 's/\r//' LICENSE.txt

# fix non ASCII chars
native2ascii -encoding UTF8 src/main/java/org/mvel2/sh/ShellSession.java src/main/java/org/mvel2/sh/ShellSession.java

%mvn_file :%{pkg_name}2 %{pkg_name}
%{?scl_disable}

%build
%{?scl_enable}
%ifarch %{arm}
# Tests fails only on ARM builder
%mvn_build -f
%else
%mvn_build
%endif
%{?scl_disable}

%install
%{?scl_enable}
%mvn_install

%{!?scl:mkdir -p %{buildroot}%{_bindir}}
%{?scl:mkdir -p %{buildroot}%{_root_bindir}}
%{!?scl:install -pm 755 %{SOURCE1} %{buildroot}%{_bindir}/%{pkg_name}}
%{?scl:install -pm 755 %{SOURCE1} %{buildroot}%{_root_bindir}/%{pkg_name}}
%{?scl_disable}

%files -f .mfiles
%{!?scl:%{_bindir}/%{pkg_name}}
%{?scl:%{_root_bindir}/%{pkg_name}}
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed Sep 21 2016 Tomas Repik <trepik@redhat.com> - 2.2.7-3
- scl conversion
- removed bundled asm

* Thu Jun 30 2016 gil cattaneo <puntogil@libero.it> 2.2.7-2
- add missing build requires

* Thu Feb 11 2016 gil cattaneo <puntogil@libero.it> 2.2.7-1
- update to 2.2.7.Final

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 25 2015 gil cattaneo <puntogil@libero.it> 2.2.6-1
- update to 2.2.6.Final

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 10 2015 gil cattaneo <puntogil@libero.it> 2.2.2-2
- introduce license macro

* Thu Dec 18 2014 gil cattaneo <puntogil@libero.it> 2.2.2-1
- update to 2.2.2.Final

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 gil cattaneo <puntogil@libero.it> 2.1.6-2
- fix rhbz#1095339

* Mon Sep 16 2013 gil cattaneo <puntogil@libero.it> 2.1.6-1
- update to 2.1.6.Final

* Fri Jul 05 2013 gil cattaneo <puntogil@libero.it> 2.0.19-5
- switch to XMvn
- minor changes to adapt to current guideline

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.0.19-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 26 2012 gil cattaneo <puntogil@libero.it> 2.0.19-1
- initial rpm
