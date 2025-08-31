Name:           cursor
Version:        1.5.9
Release:        1%{?dist}
Summary:        Cursor - The AI Code Editor

License:        LicenseRef-Proprietary
URL:            https://www.cursor.com/
Source0:        Cursor-1.5.9-x86_64.AppImage

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

%files
/lib64/libffmpeg.so
/usr/local/cursor/*
/usr/local/bin/cursor
/usr/share/applications/cursor.desktop
/usr/share/icons/hicolor/*/apps/cursor.png
/usr/share/pixmaps/co.anysphere.cursor.png
