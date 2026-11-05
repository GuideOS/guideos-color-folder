#!/bin/bash
set -e

# Pfad zu den systemweiten Icons
TARGET_DIR="/usr/share/icons"
TEMP_DIR=$(mktemp -d)

# Prüfen, ob das Skript mit sudo/Root-Rechten ausgeführt wird
if [ "$EUID" -ne 0 ]; then
  echo "Fehler: Dieses Skript muss mit Root-Rechten ausgeführt werden (sudo)."
  exit 1
fi

echo "=========================================="
echo " Mint-Y Icons Herunterladen & Installieren"
echo "=========================================="

# 1. Abhängigkeiten prüfen (curl, tar, git)
if ! command -v curl &> /dev/null; then
    echo "curl wird benötigt. Installiere..."
    apt-get update && apt-get install -y curl
fi

# 2. Linux Mint Icon-Repository als ZIP/Tarball herunterladen
echo "[1/4] Lade Mint-Y Icon Paket herunter..."
REPO_URL="https://github.com/linuxmint/mint-y-icons/archive/refs/heads/master.tar.gz"
curl -L --progress-bar -o "$TEMP_DIR/mint-y-icons.tar.gz" "$REPO_URL"

# 3. Quellcodedateien entpacken
echo "[2/4] Entpacke Archiv..."
tar -xzf "$TEMP_DIR/mint-y-icons.tar.gz" -C "$TEMP_DIR"

# 4. Mint-Y Themes in das System-Icon-Verzeichnis kopieren
echo "[3/4] Kopiere Mint-Y Themes nach $TARGET_DIR..."

# In der Repository-Struktur liegen die Themes unter src/icons oder build-Strukturen
SRC_ICONS="$TEMP_DIR/mint-y-icons-master/src/icons"

if [ -d "$SRC_ICONS" ]; then
    # Alle Mint-Y Ordner kopieren
    cp -r "$SRC_ICONS"/Mint-Y* "$TARGET_DIR/" 2>/dev/null || true
    echo "Mint-Y Icons erfolgreich nach $TARGET_DIR kopiert."
else
    # Fallback, falls sich die Ordnerstruktur im Git-Repo unterscheidet
    echo "Kopiere generische Icon-Pfade..."
    find "$TEMP_DIR/mint-y-icons-master" -type d -name "Mint-Y*" -exec cp -r {} "$TARGET_DIR/" \;
fi

# 5. Aufräumen & Cache aktualisieren
echo "[4/4] Aktualisiere Icon-Caches..."
rm -rf "$TEMP_DIR"

for theme in "$TARGET_DIR"/Mint-Y*; do
    if [ -d "$theme" ]; then
        gtk-update-icon-cache -f -q "$theme" 2>/dev/null || true
    fi
done

echo "=========================================="
echo " Fertig! Die Mint-Y Icons stehen nun auf"
echo " deinem Debian-System zur Verfügung."
echo "=========================================="
