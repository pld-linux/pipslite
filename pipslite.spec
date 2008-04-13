Summary:	Photo Image Print System Lite for Linux
Summary(pl.UTF-8):	System druku fotograficznego dla Linuksa
Name:		pipslite
Version:	1.0.2
Release:	1
License:	Mixed (GPL, LGPL, distributable)
Group:		Applications/Printing
Source0:	http://lx2.avasys.jp/pips/lite%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}-ekpd.init
Patch0:		%{name}-services.patch
Patch1:		%{name}-ekpd-permissions.patch             
Patch2:		%{name}-init.patch
URL:		http://www.avasys.jp/english/linux_e/dl_spc.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel >= 0.99.7
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.174
BuildRequires:	sed >= 4.0
Requires:	cups-filter-pstoraster
Requires:	ghostscript
Requires(post,preun):	/sbin/chkconfig
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This software is a Printer Driver (filter) for the high quality print
with SEIKO EPSON Color Ink Jet Printer from the Linux.

This product supports only EPSON ESC/P-R printers. Its function is
same as Photo Image Print System. Unlike Photo Image Print System,
which requires different package for each printer model, only one
pipslite package can be used for all EPSON ESC/P-R printers.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik drukarki (filtr) do wydruków wysokiej
jakości na drukarkach atramentowych SEIKO EPSON Color Ink Jet Printer
z poziomu Linuksa.

Ten produkt obsługuje tylko drukarki EPSON ESC/P-R. Ma funkcje takie
same jak Photo Image Print System; w przeciwieństwie do niego nie
wymaga innego pakietu dla każdego modelu drukarki, istnieje tylko
jeden pakiet pipslite, który może być używany na wszystkich drukarkach
EPSON ESC/P-R.

%package cups
Summary:	Cups binding of Epson print system
Summary(pl.UTF-8):	Dowiązania systemu druku Epson dla cupsa
Group:		Applications/Printing
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description cups
Cups binding of Epson print system.

%description cups -l pl.UTF-8
Dowiązania systemu druku Epson dla cupsa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ekpd
:> $RPM_BUILD_ROOT%{_sysconfdir}/pipsrc
mv $RPM_BUILD_ROOT%{_libdir}/pipslite/ekpd $RPM_BUILD_ROOT%{_sbindir}

rm -rf $RPM_BUILD_ROOT%{_datadir}/pipslite/{rc.d,readme}

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/zh{,_CN}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ekpd
if [ -f /var/lock/subsys/ekpd ]; then
	/etc/rc.d/init.d/ekpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/ekpd start\" to start EPSON KOWA Printer Daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ekpd ]; then
		/etc/rc.d/init.d/ekpd stop 1>&2
	fi
	/sbin/chkconfig --del ekpd
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING*
%doc doc/readmelite doc/readmelite.ja
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pipslite/ekpdrc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pipsrc
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/ekpd
%attr(754,root,root) /etc/rc.d/init.d/ekpd
%attr(755,root,root) %{_libdir}/pipslite/*
%attr(755,root,root) %{_libdir}/liblite.so*
%{_libdir}/liblite.la
%attr(600,lp,lp) %{_var}/run/*
%dir %{_datadir}/pipslite
%{_datadir}/pipslite/paper_list.csv
%dir %{_datadir}/pipslite
%dir %{_datadir}/pipslite/scripts
%{_datadir}/pipslite/scripts/*.lc
%attr(755,root,root) %{_datadir}/pipslite/scripts/setup-lpr.sh
%attr(755,root,root) %{_datadir}/pipslite/scripts/inst-lpr-post.sh

%files cups
%defattr(644,root,root,755)
%doc doc/readmelite-cups*
%attr(755,root,root) %{_libdir}/cups/backend/*
%attr(755,root,root) %{_libdir}/cups/filter/*
%{_datadir}/cups/model/*
%attr(755,root,root) %{_datadir}/pipslite/scripts/setup-cups.sh
%attr(755,root,root) %{_datadir}/pipslite/scripts/inst-cups-post.sh
