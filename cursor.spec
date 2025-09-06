Name:           cursor
Version:        1.5.11
Release:        1%{?dist}
Summary:        Cursor - The AI Code Editor

License:        LicenseRef-Proprietary
URL:            https://www.cursor.com/
Source0:        Cursor-1.5.11-x86_64.AppImage

BuildArch:      x86_64
ExclusiveArch:  x86_64

%description
Built to make you extraordinarily productive, Cursor is the best way to code with AI.

%prep
# No prep required

%build
# No build required

%install
chmod +x %{SOURCE0}
%{SOURCE0} --appimage-extract

# Install main application files
mkdir -p %{buildroot}/usr/local/cursor/
cp -r squashfs-root/* %{buildroot}/usr/local/cursor/

# Install libffmpeg
mkdir -p %{buildroot}/lib64
cp squashfs-root/usr/share/cursor/libffmpeg.so %{buildroot}/lib64/libffmpeg.so

# Install hicolor theme icons
mkdir -p %{buildroot}/usr/share/icons/hicolor/
cp -r squashfs-root/usr/share/icons/hicolor/* %{buildroot}/usr/share/icons/hicolor/

# Install the specifically named icon to /usr/share/pixmaps
mkdir -p %{buildroot}/usr/share/pixmaps
cp squashfs-root/usr/share/pixmaps/co.anysphere.cursor.png %{buildroot}/usr/share/pixmaps/co.anysphere.cursor.png

mkdir -p %{buildroot}/usr/share/applications/
cp squashfs-root/cursor.desktop %{buildroot}/usr/share/applications/cursor.desktop

# Create symlink for the executable
mkdir -p %{buildroot}/usr/local/bin/
ln -sf /usr/local/cursor/AppRun %{buildroot}/usr/local/bin/cursor

%post
gtk-update-icon-cache -f -t /usr/share/icons/hicolor || : # Update hicolor cache

%posttrans
# One-time deprecation notice on upgrade
_markdir=%{_localstatedir}/lib/%{name}
_marker=${_markdir}/.deprecated_notice_shown
if [ "$1" -eq 2 ]; then # 2 = upgrade
  mkdir -p "${_markdir}"
  if [ ! -f "${_marker}" ]; then
    cat >&2 <<'EOF'
DEPRECATED: This COPR repackaged Cursor from AppImage. Cursor now ships the official RPM on their website.
Migrate to the official package:
  https://forum.cursor.com/t/linux-deb-and-rpm-downloads/132054
Project: https://github.com/waaiez/cursor-copr-build
Official: https://www.cursor.com/downloads
EOF
    : > "${_marker}"
  fi
fi

%preun
# On erase, clean the marker
if [ "$1" -eq 0 ]; then
  rm -f %{_localstatedir}/lib/%{name}/.deprecated_notice_shown || :
fi

%files
/lib64/libffmpeg.so
/usr/local/cursor/*
/usr/local/bin/cursor
/usr/share/applications/cursor.desktop
/usr/share/icons/hicolor/*/apps/cursor.png
/usr/share/pixmaps/co.anysphere.cursor.png
