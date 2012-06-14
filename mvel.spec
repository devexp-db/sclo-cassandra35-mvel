
Name:          mvel
Version:       2.0.19
Release:       1%{?dist}
Summary:       MVFLEX Expression Language
Group:         Development/Libraries
License:       ASL 2.0
Url:           http://mvel.codehaus.org/
# git clone git://github.com/mikebrock/mvel.git mvel2-2.0.18
# cd mvel-2.0.19/ && git archive --format=tar --prefix=mvel2-2.0.19/ mvel2-2.0.19 | xz > ../mvel2-2.0.19.tar.xz
Source0:       %{name}-%{version}.tar.xz
Source1:       mvel-script
Patch0:        mvel-2.0.19-use-system-asm.patch
# remove tests which require internal objectweb-asm libraries
Patch1:        mvel-2.0.19-tests.patch
BuildRequires: java-devel
BuildRequires: jpackage-utils

BuildRequires: objectweb-asm

# test deps 
BuildRequires: junit
BuildRequires: xstream

BuildRequires: maven
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit4
BuildRequires: maven-surefire-report-plugin

Requires:      objectweb-asm

Requires:      java
Requires:      jpackage-utils
BuildArch:     noarch

%description
MVEL is a powerful expression language for Java-based applications. It
provides a plethora of features and is suited for everything from the
smallest property binding and extraction, to full blown scripts.

%package javadoc
Group:         Documentation
Summary:       Javadoc for %{name}
Requires:      jpackage-utils

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
find . -name "*.jar" -delete
find . -name "*.class" -delete
rm ASM-LICENSE.txt
%patch0 -p1
%patch1 -p0

sed -i 's/\r//' LICENSE.txt

# fix non ASCII chars
native2ascii -encoding UTF8 src/main/java/org/mvel2/sh/ShellSession.java src/main/java/org/mvel2/sh/ShellSession.java

%build
# some test at random fails
mvn-rpmbuild -Dproject.build.sourceEncoding=UTF-8 -Dmaven.test.failure.ignore=true install javadoc:aggregate

%install

mkdir -p %{buildroot}%{_javadir}
install -pm 644 target/%{name}2-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/api*/* %{buildroot}%{_javadocdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
install -pm 755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%{_javadir}/%{name}*.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
* Sat May 26 2012 gil cattaneo <puntogil@libero.it> 2.0.19-1
- initial rpm

