# GuideOS Color Folder

**GuideOS Color Folder** ist eine Nemo-Aktion für Debian (getestet auf GuideOS 1.1), mit der du die Ordnerfarben im Cinnamon-Dateimanager (Nemo) ganz unkompliziert per Rechtsklick ändern kannst. Das Paket installiert sich nahtlos und lädt für eine größere Auswahl die Mint-Y-Icons direkt aus dem Netz nach.

---

## Funktionen

* **Rechtsklick-Integration:** Ändere die Farbe einzelner oder mehrerer Ordner direkt über das Nemo-Kontextmenü.
* **Automatische Icon-Beschaffung:** Lädt die offiziellen Mint-Y-Icon-Themes dynamisch während der Installation herunter (falls noch nicht geschehen).
* **Saubere Paketverwaltung:** Vollständig in das Debian-Paketmanagement integriert (`.deb`). Bei einer Deinstallation werden heruntergeladene Icons sauber wieder entfernt.
* **Fehlertolerant:** Schlägt die Installation fehl (z. B. keine Internetverbindung), bricht das `.deb`-Paket nicht ab, sondern installiert die Grundfunktion reibungslos.

---
## 🔧 Installation

#### Download des `.deb` Packages, von der **[Releases](https://github.com/Nightworker-DE/guideos-color-folder/releases)** Section in diesem Repository

Installiere das generierte Paket mit `apt`:

```bash
sudo apt install ./guideos-color-folder*.deb
```

_Hinweis während der Installation:_ Das `postinst`-Skript prüft, ob eine Internetverbindung besteht, und lädt das `mint-y-icons`-Repository herunter, um die Farb-Icons nach `/usr/share/icons/` zu entpacken.

## Deinstallation

Wenn du das Paket wieder entfernen möchtest, reicht ein:

```bash
sudo apt remove guideos-color-folder
```


Dank des `postrm`-Skripts werden dabei auch alle dynamisch heruntergeladenen Mint-Y-Ordnerfarben-Icons restlos von deinem System entfernt.
