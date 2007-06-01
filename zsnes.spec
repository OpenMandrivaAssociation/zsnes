%define name zsnes
%define version 1.51
%define release %mkrel 3
%define fversion %(echo %version|sed s/\\\\\.//)
%define dversion %(echo %version|sed s/\\\\\./_/)

Summary: Nintendo Super NES / Super Famicom Emulator
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownloads.sourceforge.net/zsnes/%{name}%{fversion}src.tar.bz2
Patch: zsnes150-desktop.patch
Source1: %{name}-icons.tar.bz2
License: GPL
Group: Emulators
BuildRoot: %{_tmppath}/%{name}-buildroot
URL: http://zsnes.sourceforge.net
BuildRequires: nasm
BuildRequires: libpng-devel
BuildRequires: libSDL-devel >= 1.2 
BuildRequires: libmesagl-devel
BuildRequires: libncurses-devel
BuildRequires: libao-devel
Epoch: 1

%description
This is an emulator for Nintendo's 16 bit console, called Super Nintendo 
Entertainment System or Super Famicom. It features a pretty accurate emulation
of that system's graphic and sound capabilities.
The GUI enables the user to select games, change options, enable cheat codes 
and to save the game state, even network play is possible.


%prep

%setup -q -n %{name}_%dversion
%patch -p1
cd src
./autogen.sh

%build
cd src
# zsnes do not work with fortify patch, and i frankly do not want to mess with the mix of asm and C source code
# (misc)
export CFLAGS="-O2 -g -pipe -fexceptions -fomit-frame-pointer -fasynchronous-unwind-tables"
%configure --x-includes=/usr/X11R6/include --enable-release --enable-libao --disable-cpucheck force_arch=i586 
make

%install
rm -rf %buildroot
mkdir -p %buildroot%{_bindir}
install -c -m 0755 src/zsnes %buildroot%{_bindir}

mkdir -p %buildroot%{_mandir}/man1/
install -c -m 0644 src/linux/zsnes.1 %buildroot%{_mandir}/man1

install -m 644 -D src/linux/zsnes.desktop %buildroot%_datadir/applications/zsnes.desktop

# install icons
install -m 755 -d %buildroot{%{_miconsdir},%{_iconsdir},%{_liconsdir}}
tar xOjf %SOURCE1 %{name}-16x16.png > %buildroot%{_miconsdir}/%{name}.png
tar xOjf %SOURCE1 %{name}-32x32.png > %buildroot%{_iconsdir}/%{name}.png
tar xOjf %SOURCE1 %{name}-48x48.png > %buildroot%{_liconsdir}/%{name}.png

%clean
rm -rf %buildroot

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%doc docs/*
%{_bindir}/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/%name.1*
%_datadir/applications/%name.desktop


