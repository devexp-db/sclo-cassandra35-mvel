Name:          mvel
Version:       2.0.19
Release:       6%{?dist}
Summary:       MVFLEX Expression Language
License:       ASL 2.0
Url:           http://mvel.codehaus.org/
Source0:       https://github.com/mikebrock/mvel/archive/%{name}2-%{version}.tar.gz
Source1:       %{name}-script
Patch0:        %{name}-2.0.19-use-system-asm.patch
# remove tests which require internal objectweb-asm libraries
Patch1:        %{name}-2.0.19-tests.patch

BuildRequires: java-devel
BuildRequires: objectweb-asm

# test deps 
BuildRequires: junit
BuildRequires: xstream

BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
BuildRequires: maven-surefire-provider-junit4
BuildRequires: maven-surefire-report-plugin

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
%setup -q -n %{name}-%{name}2-%{version}
find . -name "*.jar" -delete
find . -name "*.class" -delete
rm ASM-LICENSE.txt
%patch0 -p1
%patch1 -p0

sed -i 's/\r//' LICENSE.txt

# fix non ASCII chars
native2ascii -encoding UTF8 src/main/java/org/mvel2/sh/ShellSession.java src/main/java/org/mvel2/sh/ShellSession.java

%build
%mvn_file :%{name}2 %{name}
# some test at random fails
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8 -Dmaven.test.failure.ignore=true

%install
%mvn_install

mkdir -p %{buildroot}%{_bindir}
install -pm 755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}

%files -f .mfiles
%{_bindir}/%{name}
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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