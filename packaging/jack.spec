%global groupname audio
%global pagroup   pulse-rt

Summary:       The Audio Connection Kit
Name:          jack
Version:       1.9.9.5
Release:       0
License:       GPL-2.0+
Group:         Multimedia/Audio
URL:           http://www.jackaudio.org
Source0:       %{name}-%{version}.tar.bz2
Source100:     jack-limits.conf
Source1001:    jack.manifest
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(celt)
BuildRequires: doxygen
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(samplerate)
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig
BuildRequires: python
BuildRequires: readline-devel

Requires: util-linux
Requires: pwdutils
Requires:      pam

%description
JACK is a low-latency audio server, written primarily for the Linux operating
system. It can connect a number of different applications to an audio device, as
well as allowing them to share audio between themselves. Its clients can run in
their own processes (i.e. as a normal application), or can they can run within a
JACK server (i.e. a "plugin").

JACK is different from other audio server efforts in that it has been designed
from the ground up to be suitable for professional audio work. This means that
it focuses on two key areas: synchronous execution of all clients, and low
latency operation.

%package dbus
Summary:       Jack D-Bus launcher
Group:         Applications/Multimedia
Requires:      %{name} = %{version}-%{release}

%description dbus
Launcher to start Jack through D-Bus.


%package devel
Summary:       Header files for Jack
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description devel
Header files for the Jack Audio Connection Kit.

%package example-clients
Summary:       Example clients that use Jack
Group:         Applications/Multimedia
Requires:      %{name} = %{version}-%{release}

%description example-clients
Small example clients that use the Jack Audio Connection Kit.

%prep
%setup -q -n jack-%{version}

cp %{SOURCE1001} .
sed -i 's/\r$//' README

%build
export CPPFLAGS="$RPM_OPT_FLAGS -O0"
export PREFIX=%{_prefix}
# Parallel build disabled as it fails sometimes
./waf configure \
  %{?_smp_mflags} \
  --libdir=%{_libdir} \
  --classic \
  --alsa \
  --dbus \
  --clients 256 \
  --ports-per-application=2048

./waf build %{?_smp_mflags} -v

%install
./waf --destdir=%{buildroot} install

# install our limits to the /etc/security/limits.d
mkdir -p %{buildroot}%{_sysconfdir}/security/limits.d
sed -e 's,@groupname@,%groupname,g; s,@pagroup@,%pagroup,g;' \
    %{SOURCE100} > %{buildroot}%{_sysconfdir}/security/limits.d/95-jack.conf

# For compatibility with jack1
mv %{buildroot}%{_bindir}/jack_rec %{buildroot}%{_bindir}/jackrec

# Fix permissions of the modules
chmod 755 %{buildroot}%{_libdir}/jack/*.so %{buildroot}%{_libdir}/libjack*.so.*.*.*

%pre
getent group %groupname > /dev/null || groupadd -r %groupname
exit 0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README README_NETJACK2
%{_bindir}/jackd
%{_bindir}/jackrec
%{_libdir}/jack/
%{_libdir}/libjack.so.*
%{_libdir}/libjacknet.so.*
%{_libdir}/libjackserver.so.*
%config(noreplace) %{_sysconfdir}/security/limits.d/*.conf


%files dbus
%{_bindir}/jackdbus
%{_datadir}/dbus-1/services/org.jackaudio.service
%{_bindir}/jack_control

%files devel
%{_includedir}/jack/
%{_libdir}/libjack.so
%{_libdir}/libjacknet.so
%{_libdir}/libjackserver.so
%{_libdir}/pkgconfig/jack.pc

%files example-clients
%{_bindir}/alsa_in
%{_bindir}/alsa_out
%{_bindir}/jack_alias
%{_bindir}/jack_bufsize
%{_bindir}/jack_connect
%{_bindir}/jack_disconnect
%{_bindir}/jack_cpu_load
%{_bindir}/jack_evmon
%{_bindir}/jack_freewheel
%{_mandir}/man1/*
%{_bindir}/jack_latent_client
%{_bindir}/jack_load
%{_bindir}/jack_unload
%{_bindir}/jack_lsp
%{_bindir}/jack_metro
%{_bindir}/jack_midi_dump
%{_bindir}/jack_midi_latency_test
%{_bindir}/jack_midiseq
%{_bindir}/jack_midisine
%{_bindir}/jack_monitor_client
%{_bindir}/jack_net_master
%{_bindir}/jack_net_slave
%{_bindir}/jack_netsource
%{_bindir}/jack_samplerate
%{_bindir}/jack_server_control
%{_bindir}/jack_session_notify
%{_bindir}/jack_showtime
%{_bindir}/jack_simple_client
%{_bindir}/jack_simple_session_client
%{_bindir}/jack_thru
%{_bindir}/jack_transport
%{_bindir}/jack_wait
%{_bindir}/jack_zombie


# tests
%{_bindir}/jack_cpu
%{_bindir}/jack_iodelay
%{_bindir}/jack_multiple_metro
%{_bindir}/jack_test
