%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define fversion %(echo %version|sed s/\\\\\.//)
%define dversion %(echo %version|sed s/\\\\\./_/)

Summary:	Nintendo Super NES / Super Famicom Emulator
Name:		zsnes
Version:	1.51
Release:	14
Epoch:		1
License:	GPLv2+
Group:		Emulators
Url:		http://zsnes.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/zsnes/%{name}%{fversion}src.tar.bz2
Source1:	%{name}-icons.tar.bz2
Patch0:		zsnes150-desktop.patch
Patch1:		zsnes-1.51-libao.patch
Patch2:		zsnes-1.51-gcc43.patch
Patch3:		zsnes-1.51-libpng15.patch
Patch4:		zsnes-1.51-gcc4.7.patch
Patch5:		zsnes-1.51-hat-events.patch
Patch6:		zsnes-1.51-matrix-init.patch
BuildRequires:	nasm
BuildRequires:	pkgconfig(ao)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(zlib)
#do not build currently on x86_64
ExclusiveArch:	%{ix86}

%description
This is an emulator for Nintendo's 16 bit console, called Super Nintendo
Entertainment System or Super Famicom. It features a pretty accurate emulation
of that system's graphic and sound capabilities.
The GUI enables the user to select games, change options, enable cheat codes
and to save the game state, even network play is possible.

%files
%doc docs/*
%{_bindir}/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/%{name}.desktop

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}_%{dversion}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
find . -name "Makefile*" -o -name "*.m4" |xargs sed -i -e 's,configure.in,configure.ac,g'
cd src
autoreconf -fiv
# zsnes do not work with fortify patch, and i frankly do not want to mess with the mix of asm and C source code
# (misc)
export CFLAGS="-O2 -g -pipe -fexceptions -fomit-frame-pointer -fasynchronous-unwind-tables"
%configure2_5x \
	--enable-libao \
	--disable-cpucheck \
	force_arch=i586
make

%install
mkdir -p %{buildroot}%{_bindir}
install -c -m 0755 src/zsnes %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_mandir}/man1/
install -c -m 0644 src/linux/zsnes.1 %{buildroot}%{_mandir}/man1

install -m 644 -D src/linux/zsnes.desktop %{buildroot}%{_datadir}/applications/zsnes.desktop

# install icons
install -m 755 -d %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir}}
tar xOjf %{SOURCE1} %{name}-16x16.png > %{buildroot}%{_miconsdir}/%{name}.png
tar xOjf %{SOURCE1} %{name}-32x32.png > %{buildroot}%{_iconsdir}/%{name}.png
tar xOjf %{SOURCE1} %{name}-48x48.png > %{buildroot}%{_liconsdir}/%{name}.png

