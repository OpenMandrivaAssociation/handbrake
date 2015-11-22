%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define lname HandBrake

Summary:	MPEG-AVC(H.264)/MPEG-4 converter
Name:		handbrake
Version:	0.10.2
Release:	1
License:	GPLv2+
Group:		Video
Url:		http://handbrake.fr/
Source0:	%{lname}-%{version}.tar.bz2

Source1:libav-v10.1.tar.bz2
Source2:libbluray-0.5.0.tar.bz2
Source3:libdvdnav-5.0.1-0-gaa3659d.tar.gz
Source4:libdvdread-5.0.0-6-gcb1ae87.tar.gz
Source5:libvpx-v1.3.0.tar.bz2
Source6:x265-9329-0d30d2641875-1.5.tar.bz2
Source7:fdk-aac-v0.1.1-6-gbae4553.tar.bz2

BuildRequires:	intltool
BuildRequires:	iso-codes
BuildRequires:	libtool
BuildRequires:	svn
BuildRequires:	valgrind
BuildRequires:	yasm
BuildRequires:	bzip2-devel
BuildRequires:	lame-devel
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(webkitgtk-3.0)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libass)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(x264)
BuildRequires:	pkgconfig(x265)

%description
HandBrake is an open-source, GPL-licensed, multi-platform,
multi-threaded MPEG-AVC(x.264)/MPEG-4 converter, available for
MacOS X, Linux and Windows. It is a video encoder that takes
your movies and transfers them to a format that's useful on
your computers, media centers, and portable electronic devices.

%files -f ghb.lang
%doc AUTHORS COPYING CREDITS NEWS THANKS TRANSLATIONS
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/hb-icon.*

#----------------------------------------------------------------------------

%prep
%setup -q -n %{lname}-%{version}
%apply_patches

find . -name "Makefile*" -o -name "*.m4" |xargs sed -i -e 's,configure.in,configure.ac,g'

mkdir download
cp -t download %{SOURCE1}
cp -t download %{SOURCE2}
cp -t download %{SOURCE3}
cp -t download %{SOURCE4}
cp -t download %{SOURCE5}
cp -t download %{SOURCE6}
cp -t download %{SOURCE7}

%build
# export CFLAGS="$RPM_OPT_FLAGS"
# export CXXFLAGS="$RPM_OPT_FLAGS"
./configure --prefix=%{_prefix} --launch --launch-jobs=0 

pushd gtk
autoreconf
popd
cd build && make

%install
%makeinstall_std -C build

install -m 0755 build/HandBrakeCLI %{buildroot}%{_bindir}/HandBrakeCLI
pushd %{buildroot}%{_bindir}
ln -s ./HandBrakeCLI ./handbrake
popd

sed -i -e "s|hb-icon|hb-icon.png|" %{buildroot}%{_datadir}/applications/ghb.desktop

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

rm -rf %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache

%find_lang ghb

