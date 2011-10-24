# This is a version of BCEL that has been modified by the findbugs team.  They
# added some new functionality and also did some performance optimizations of
# the base code.  I am not producing a new manual, since we already have a
# bcel-manual package and the findbugs team did not patch the manual.  However,
# the javadoc package is necessary to show the changes in the API created by
# the findbug team's work.

%global findbugsver 1.3.8

Name:           findbugs-bcel
Version:        5.2
Release:        %{findbugsver}
Summary:        Byte Code Engineering Library with findbugs extensions

Group:          Development/Java
License:        ASL 2.0
URL:            http://jakarta.apache.org/bcel/
Source0:        http://www.apache.org/dist/jakarta/bcel/source/bcel-%{version}-src.tar.gz
# This patch is available in the findbugs release, in src/patches/bcel.diff.
Source1:        bcel.diff

BuildRequires:  java-devel, jpackage-utils
Requires:       java, jpackage-utils

BuildArch:      noarch

%description
This is a version of Apache's Byte Code Engineering Library (BCEL) that has
been modified by the findbugs developers.  The modifications add some new
functionality, and also introduce a number of performance optimizations to
address findbugs performance problems.  Some of the performance optimizations
induce API changes, so this version of BCEL is not compatible with the vanilla
upstream version.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q -n bcel-%{version}
%{__patch} -p7 -s < %{SOURCE1}

%build
# The ant and maven builds both try to download unneeded jars
mkdir classes
find src/java -type f -name '*.java' | \
xargs javac -g -d classes -source 1.5 -encoding ISO8859-1
cd classes
jar cf findbugs-bcel-%{findbugsver}.jar org
cd ..

mkdir javadoc
find src/java -type f -name '*.java' | xargs javadoc -sourcepath src/java \
  -classpath classes -source 1.5 -encoding ISO8859-1 -d javadoc 

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p classes/findbugs-bcel-%{findbugsver}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s findbugs-bcel-%{findbugsver}.jar $RPM_BUILD_ROOT%{_javadir}/findbugs-bcel.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}
cp -a javadoc $RPM_BUILD_ROOT%{_javadocdir}/findbugs-bcel-%{findbugsver}
ln -s findbugs-bcel-%{findbugsver} $RPM_BUILD_ROOT%{_javadocdir}/findbugs-bcel

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt README.txt
%{_javadir}/findbugs-bcel*

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/findbugs-bcel*

