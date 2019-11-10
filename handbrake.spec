%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define lname HandBrake

Summary:	MPEG-AVC(H.264)/MPEG-4 converter
Name:		handbrake
Version:	1.3.0
Release:	1
License:	GPLv2+
Group:		Video
Url:		http://handbrake.fr/
Source0:	https://download.handbrake.fr/releases/%{version}/%{lname}-%{version}-source.tar.bz2

# Handbrake switch from libav to ffmpeg, so replace it.
# Use non-system ffmpeg, because currently we have 4.0.X, and needed is 4.1. (penguin)
# as of 1.3.0 - bundle ffmpeg support more features than previded by omv.
Source1:	ffmpeg-4.2.1.tar.bz2
Source2:	libbluray-1.1.2.tar.bz2
Source3:	libdvdnav-6.0.1.tar.bz2
Source4:	libdvdread-6.0.2.tar.bz2
#Source5:	libvpx-1.8.1.tar.gz
Source6:	x265_3.2.1.tar.gz
#Source7:  nv-codec-headers-9.0.18.1.tar.gz

# Source100 and patch0 for fix build on i686.
Source100:  linking-issue-on-non-x86-platform.patch
Patch0: 0001-Don-t-build-x265-10-12bit.patch

BuildRequires:  meson
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:	cmake
BuildRequires:	intltool
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:	iso-codes
BuildRequires:	libtool
BuildRequires:	svn
BuildRequires:	valgrind
BuildRequires:	yasm
BuildRequires:	bzip2-devel
BuildRequires:	lame-devel
BuildRequires:  nasm
BuildRequires:  python-devel
BuildRequires:  pkgconfig(jansson)
#BuildRequires:  pkgconfig(gthread-2.0
#BuildRequires:	ffmpeg-devel
#BuildRequires:	pkgconfig(gstreamer-%{gstapi})
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(numa)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libass)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(opus)
BuildRequires:  pkgconfig(speex)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(x264)
BuildRequires:	pkgconfig(x265)
BuildRequires:  pkgconfig(ffnvcodec)
BuildRequires:  pkgconfig(vpx)

%description
HandBrake is an open-source, GPL-licensed, multi-platform,
multi-threaded MPEG-AVC(x.264)/MPEG-4 converter, available for
MacOS X, Linux and Windows. It is a video encoder that takes
your movies and transfers them to a format that's useful on
your computers, media centers, and portable electronic devices.

%files -f ghb.lang
%doc COPYING
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/hb-icon.*
%{_iconsdir}/hicolor/scalable/apps/fr.handbrake.ghb.svg
%{_datadir}/metainfo/fr.handbrake.ghb.appdata.xml

#----------------------------------------------------------------------------

%prep
%setup -q -n %{lname}-%{version}
%ifarch %ix86
%patch0 -p1 -b .x265-no-10bit-12bit
%endif

find . -name "Makefile*" -o -name "*.m4" |xargs sed -i -e 's,configure.in,configure.ac,g'
mkdir download
cp -t download %{SOURCE1}
cp -t download %{SOURCE2}
cp -t download %{SOURCE3}
cp -t download %{SOURCE4}
#cp -t download %{SOURCE5}
cp -t download %{SOURCE6}
#cp -t download %{SOURCE7}

#import to fix i686 build
%{__cp} -a %{SOURCE100} contrib/x265/A99-linking-issue-on-non-x86-platform.patch

%build
# export CFLAGS="$RPM_OPT_FLAGS"
# export CXXFLAGS="$RPM_OPT_FLAGS"
./configure --prefix=%{_prefix} --launch --launch-jobs=0  --disable-gtk-update-checks

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

#sed -i -e "s|hb-icon|hb-icon.png|" %{buildroot}%{_datadir}/applications/ghb.desktop

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

rm -rf %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache

%find_lang ghb

