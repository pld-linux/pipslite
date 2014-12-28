Summary:	Photo Image Print System Lite for Linux
Summary(pl.UTF-8):	System druku fotograficznego dla Linuksa
Name:		pipslite
Version:	1.0.2
Release:	1
License:	GPL v2+ (programs), LGPL v2+ (library)
Group:		Applications/Printing
Source0:	http://lx2.avasys.jp/pips/lite%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}-ekpd.init
Patch0:		%{name}-services.patch
Patch1:		%{name}-ekpd-permissions.patch             
Patch2:		%{name}-init.patch
Patch3:		%{name}-link.patch
Patch4:		%{name}-system-ltdl.patch
URL:		http://www.avasys.jp/english/linux_e/dl_spc.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	gettext-tools
BuildRequires:	gtk+-devel >= 0.99.7
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.174
BuildRequires:	sed >= 4.0
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	cups-filter-pstoraster
Requires:	ghostscript
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
%patch3 -p1
%patch4 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static
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
# no devel
rm $RPM_BUILD_ROOT%{_libdir}/liblite.la

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/zh{,_CN}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
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

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS doc/readmelite
%lang(ja) %doc doc/readmelite.ja
%attr(755,root,root) %{_bindir}/ekpstm
%attr(755,root,root) %{_bindir}/pipslite
%attr(755,root,root) %{_bindir}/pipslite-install
%attr(755,root,root) %{_sbindir}/ekpd
%dir %{_libdir}/pipslite
%attr(755,root,root) %{_libdir}/pipslite/filterlite
%attr(755,root,root) %{_libdir}/pipslite/freset
%attr(755,root,root) %{_libdir}/pipslite/gsconfig
%attr(755,root,root) %{_libdir}/liblite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblite.so.1
# dlopened by .so
%attr(755,root,root) %{_libdir}/liblite.so
%dir %{_sysconfdir}/pipslite
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pipslite/ekpdrc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pipsrc
%attr(754,root,root) /etc/rc.d/init.d/ekpd
%attr(600,lp,lp) %{_var}/run/ekplp0
%dir %{_datadir}/pipslite
%{_datadir}/pipslite/paper_list.csv
%dir %{_datadir}/pipslite/scripts
%{_datadir}/pipslite/scripts/en.lc
%lang(ja) %{_datadir}/pipslite/scripts/ja.lc
%attr(755,root,root) %{_datadir}/pipslite/scripts/inst-lpr-post.sh
%attr(755,root,root) %{_datadir}/pipslite/scripts/setup-lpr.sh

%files cups
%defattr(644,root,root,755)
%doc doc/readmelite-cups
%lang(ja) %doc doc/readmelite-cups.ja
%attr(755,root,root) %{_prefix}/lib/cups/backend/ekplp
%attr(755,root,root) %{_prefix}/lib/cups/filter/pipstoprinter
%attr(755,root,root) %{_prefix}/lib/cups/filter/rastertopips
%{_datadir}/cups/model/eklite.ppd
%attr(755,root,root) %{_datadir}/pipslite/scripts/inst-cups-post.sh
%attr(755,root,root) %{_datadir}/pipslite/scripts/setup-cups.sh
