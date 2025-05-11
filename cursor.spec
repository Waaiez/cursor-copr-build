Name:           cursor
Version:        0.50.0
Release:        1%{?dist}
Summary:        Cursor - The AI Code Editor

License:        LicenseRef-Proprietary
URL:            https://www.cursor.com/
Source0:        Cursor-0.50.0-x86_64.AppImage

BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme

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

mkdir -p %{buildroot}/usr/local/cursor/
cp -r squashfs-root/* %{buildroot}/usr/local/cursor/

mkdir -p %{buildroot}/lib64
cp squashfs-root/usr/share/cursor/libffmpeg.so %{buildroot}/lib64/libffmpeg.so

ICON_NAME="co.anysphere.cursor"
ICON_SRC_FILE="squashfs-root/${ICON_NAME}.png"
ICON_SIZE_DIR="256x256"

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${ICON_SIZE_DIR}/apps/
if [ -f "${ICON_SRC_FILE}" ]; then
    cp "${ICON_SRC_FILE}" "%{buildroot}%{_datadir}/icons/hicolor/${ICON_SIZE_DIR}/apps/${ICON_NAME}.png"
else
    echo "Warning: Primary icon ${ICON_SRC_FILE} not found!"
fi

if [ -d "squashfs-root/usr/share/icons/hicolor" ]; then
    cp -r squashfs-root/usr/share/icons/hicolor/* %{buildroot}%{_datadir}/icons/hicolor/
fi

DESKTOP_FILE_SRC="squashfs-root/cursor.desktop"

sed -i 's|^Exec=.*$|Exec=cursor %F|' "${DESKTOP_FILE_SRC}"

if grep -q '^Icon=' "${DESKTOP_FILE_SRC}"; then
  sed -i 's|^Icon=.*$|Icon=co.anysphere.cursor|' "${DESKTOP_FILE_SRC}"
else
  echo "Icon=co.anysphere.cursor" >> "${DESKTOP_FILE_SRC}"
fi

if ! grep -q '^StartupWMClass=Cursor$' "${DESKTOP_FILE_SRC}"; then
    if grep -q '^StartupWMClass=' "${DESKTOP_FILE_SRC}"; then
        sed -i 's|^StartupWMClass=.*$|StartupWMClass=Cursor|' "${DESKTOP_FILE_SRC}"
    else
        echo 'StartupWMClass=Cursor' >> "${DESKTOP_FILE_SRC}"
    fi
fi

sed -i '/^X-AppImage-Version=/d' "${DESKTOP_FILE_SRC}"

sed -i '/^Actions=new-empty-window;$/d' "${DESKTOP_FILE_SRC}"
sed -i '/^\[Desktop Action new-empty-window\]/,/^$/d' "${DESKTOP_FILE_SRC}"


mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-validate "${DESKTOP_FILE_SRC}"
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
  --rebuild-mime-info-cache \
  "${DESKTOP_FILE_SRC}"

mkdir -p %{buildroot}/usr/local/bin/
ln -sf /usr/local/cursor/AppRun %{buildroot}/usr/local/bin/cursor

%post
gtk-update-icon-cache -q -f -t %{_datadir}/icons/hicolor || :
update-desktop-database -q %{_datadir}/applications || :

%postun
if [ $1 -eq 0 ] ; then
  gtk-update-icon-cache -q -f -t %{_datadir}/icons/hicolor || :
  update-desktop-database -q %{_datadir}/applications || :
fi

%files
/lib64/libffmpeg.so
/usr/local/cursor/*
/usr/local/bin/cursor
%{_datadir}/applications/cursor.desktop
%{_datadir}/icons/hicolor/256x256/apps/co.anysphere.cursor.png
%{_datadir}/icons/hicolor/*/apps/cursor.png
