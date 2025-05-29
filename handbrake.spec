%undefine _debugsource_packages

%define _disable_lto 1

%define lname HandBrake

Summary:	MPEG-AVC(H.264)/MPEG-4 converter
Name:		handbrake
Version:	1.9.2
Release:	4
License:	GPLv2+
Group:		Video
Url:		https://handbrake.fr/
Source0:	https://download.handbrake.fr/releases/%{version}/%{lname}-%{version}-source.tar.bz2

# Handbrake switch from libav to ffmpeg, so replace it.
# Use non-system ffmpeg, bc it support more restricted features than provided by omv.
#Source1:	ffmpeg-6.1.tar.bz2
Source2:	libbluray-1.3.4.tar.bz2
Source3:	libdvdnav-6.1.1.tar.bz2
Source4:	libdvdread-6.1.3.tar.bz2
#Source6:	x265_3.6.tar.gz
#Source8:  	AMF-1.4.30-slim.tar.gz
#Source9:	dovi_tool-libdovi-3.2.0.tar.gz

# Source100 and patch0 for fix build on i686.
#Source100:  linking-issue-on-non-x86-platform.patch
#Patch0: 0001-Don-t-build-x265-10-12bit.patch

#Patch0:		https://github.com/HandBrake/HandBrake/commit/855f51bfb392cb122a7b188877b475e3b5baddde.patch

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
BuildRequires:	amf-devel
BuildRequires:  python-devel
BuildRequires:  pkgconfig(jansson)
#BuildRequires:  pkgconfig(gthread-2.0
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fribidi)
#BuildRequires:	pkgconfig(gstreamer-%{gstapi})
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(libass)
BuildRequires:	pkgconfig(dav1d)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(libturbojpeg)
BuildRequires:  pkgconfig(numa)
BuildRequires:  pkgconfig(fdk-aac)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(dbus-glib-1)
#BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(opus)
BuildRequires:  pkgconfig(speex)
BuildRequires:	pkgconfig(SvtAv1Enc)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(x264)
BuildRequires:	pkgconfig(x265)
BuildRequires:  pkgconfig(ffnvcodec)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(dovi)
%ifnarch %arm %armx
BuildRequires:  pkgconfig(libmfx)
BuildRequires:  pkgconfig(igdgmm)
BuildRequires:  pkgconfig(vpl)
%endif

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
#{_datadir}/icons/hicolor/*/apps/hb-icon.*
%{_iconsdir}/hicolor/scalable/apps/fr.handbrake.ghb.svg
%{_datadir}/metainfo/fr.handbrake.ghb.metainfo.xml

#----------------------------------------------------------------------------

%prep
%setup -q -n %{lname}-%{version}
%autopatch -p1
#ifarch %ix86
#patch0 -p1 -b .x265-no-10bit-12bit
#endif

find . -name "Makefile*" -o -name "*.m4" |xargs sed -i -e 's,configure.in,configure.ac,g'
mkdir download
#cp -t download %{SOURCE1}
cp -t download %{SOURCE2}
cp -t download %{SOURCE3}
cp -t download %{SOURCE4}
#cp -t download %{SOURCE6}
#cp -t download %{SOURCE8}
#cp -t download %{SOURCE9}

#import to fix i686 build
#{__cp} -a %{SOURCE100} contrib/x265/A99-linking-issue-on-non-x86-platform.patch

%build
# VCE is AMD specific, QSV is Intel specific. Neither will work
# on ARM or RISC-V.
./configure \
	--prefix=%{_prefix} \
	--launch \
	--launch-jobs=0 \
%ifarch %{x86_64}
	--enable-vce \
	--enable-qsv \
%else
	--disable-vce \
	--disable-qsv \
%endif
	--enable-fdk-aac

#pushd gtk
#meson -Dgtk4=true
#meson_build
#popd
cd build && make

%install
%make_install -C build

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

