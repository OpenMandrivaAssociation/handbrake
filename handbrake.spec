%define lname   HandBrake

%define major           1
%define libname		%mklibname %{name} %{major}
%define libnamedev	%mklibname %{name} %{major} -d

Summary:	MPEG-AVC(H.264)/MPEG-4 converter
Name:		handbrake
Version:	0.9.9
Release:	1
License:	GPLv2+
Group:		Video
URL:		http://handbrake.fr/
Source0:	%{lname}-%{version}.tar.bz2
BuildRequires:	yasm
BuildRequires:	zlib1-devel
BuildRequires:	bzip2-devel
BuildRequires:	intltool
BuildRequires:	svn
BuildRequires:	iso-codes
BuildRequires:	valgrind
BuildRequires:	libtool
BuildRequires:	libgstreamer0.10-plugins-base-devel
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(libgtkhtml-3.14)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(webkit-1.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libass)
BuildRequires:	pkgconfig(vorbis)

%description
HandBrake is an open-source, GPL-licensed, multi-platform,
multi-threaded MPEG-AVC(x.264)/MPEG-4 converter, available for MacOS
X, Linux and Windows. It is a video encoder that takes your
movies and transfers them to a format that's useful on your
computers, media centers, and portable electronic devices.

%prep
%setup -q -n %{lname}-%{version}
#fix encoding of non-utf8 files
#doesn't work, iconv detects illegal input sequence, --silent doesn't exist anymoreq
#iconv -t utf-8 $RPM_BUILD_DIR/%lname-%version/CREDITS
#iconv -t utf-8 $RPM_BUILD_DIR/%lname-%version/THANKS

%build
# export CFLAGS="$RPM_OPT_FLAGS"
# export CXXFLAGS="$RPM_OPT_FLAGS"
./configure --prefix=%{_prefix} --launch --launch-jobs=0 --enable-ff-mpeg2
 
cd build && make 
cd .

%install
cd build
%makeinstall_std 

install -m 0755 HandBrakeCLI %{buildroot}/%{_bindir}/HandBrakeCLI
cd %{buildroot}/%{_bindir}
ln -s ./HandBrakeCLI ./handbrake
cd -

sed -i -e "s|hb-icon|hb-icon.png|" %{buildroot}%{_datadir}/applications/ghb.desktop

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

rm -rf %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache

%clean

%files
%doc AUTHORS COPYING CREDITS NEWS THANKS TRANSLATIONS
%_bindir/*
%_datadir/applications/*
%_datadir/icons/hicolor/*/apps/hb-icon.png
