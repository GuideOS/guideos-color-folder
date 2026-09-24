#!/usr/bin/env python3
import sys
import os
import subprocess
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, Gio

# 16 Standardfarben (kompatibel mit Papirus & Mint-Y)
PALETTE = [
    ("Blue", "#42a5f5", "blue"),
    ("Blue-Grey", "#607d8b", "bluegrey"),
    ("Teal", "#009688", "teal"),
    ("Green", "#66bb6a", "green"),
    ("Yellow", "#ffee58", "yellow"),
    ("Orange", "#ffa726", "orange"),
    ("Red", "#ef5350", "red"),
    ("Pink", "#ec407a", "pink"),
    ("Magenta", "#ab47bc", "magenta"),
    ("Purple", "#7e57c2", "purple"),
    ("Violet", "#673ab7", "violet"),
    ("Indigo", "#3f51b5", "indigo"),
    ("Cyan", "#00bcd4", "cyan"),
    ("Brown", "#8d6e63", "brown"),
    ("Grey", "#bdbdbd", "grey"),
    ("Black", "#424242", "black"),
]

class ColorPickerWindow(Gtk.ApplicationWindow):
    def __init__(self, app, target_path):
        super().__init__(application=app, title="Ordnerfarbe")
        self.target_path = os.path.abspath(target_path)

        # Kompakte Fenstergröße für 16 Kacheln (4x4)
        self.set_default_size(240, 210)
        self.set_resizable(False)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        self.set_child(box)

        # Ordnername oben anzeigen
        folder_name = os.path.basename(self.target_path)
        label = Gtk.Label(label=f"<b>{folder_name}</b>")
        label.set_use_markup(True)
        box.append(label)

        # Farb-Grid (4 Spalten x 4 Zeilen)
        grid = Gtk.Grid()
        grid.set_column_spacing(6)
        grid.set_row_spacing(6)
        grid.set_halign(Gtk.Align.CENTER)
        box.append(grid)

        cols = 4
        for idx, (name, hex_code, color_key) in enumerate(PALETTE):
            btn = Gtk.Button()
            btn.set_tooltip_text(name)

            # Rechteckige Kacheln (34x24 Pixel)
            btn.set_size_request(34, 24)

            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(
                f"""
                button {{
                    background-color: {hex_code};
                    border-radius: 4px;
                    border: 1px solid rgba(0, 0, 0, 0.25);
                    padding: 0px;
                }}
                button:hover {{
                    border: 2px solid #ffffff;
                }}
                """.encode('utf-8')
            )
            btn.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

            btn.connect("clicked", self.on_color_selected, color_key)
            grid.attach(btn, idx % cols, idx // cols, 1, 1)

        # Button zum Zurücksetzen auf die Standardfarbe
        reset_btn = Gtk.Button(label="Standard zurücksetzen")
        reset_btn.set_margin_top(4)
        reset_btn.connect("clicked", self.on_reset_clicked)
        box.append(reset_btn)

    def apply_icon(self, icon_name):
        if icon_name:
            # Eventuell gesetztes festes Bild-Icon löschen und Icon-Namen setzen
            subprocess.run(["gio", "set", "-t", "unset", self.target_path, "metadata::custom-icon"], check=False)
            subprocess.run(["gio", "set", "-t", "string", self.target_path, "metadata::custom-icon-name", icon_name], check=False)
        else:
            # Metadaten zurücksetzen
            subprocess.run(["gio", "set", "-t", "unset", self.target_path, "metadata::custom-icon-name"], check=False)
            subprocess.run(["gio", "set", "-t", "unset", self.target_path, "metadata::custom-icon"], check=False)

        # Nemo-Aktualisierung auslösen
        subprocess.run(["touch", self.target_path], check=False)
        self.close()

    def on_color_selected(self, button, color_key):
        icon_name = f"folder-{color_key}"
        self.apply_icon(icon_name)

    def on_reset_clicked(self, button):
        self.apply_icon(None)

class ColorPickerApp(Gtk.Application):
    def __init__(self, target_path):
        super().__init__(application_id="org.nemo.foldercolorpicker")
        self.target_path = target_path

    def do_activate(self):
        win = ColorPickerWindow(self, self.target_path)
        win.present()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Fehler: Kein Pfad übergeben.")
        sys.exit(1)

    app = ColorPickerApp(sys.argv[1])
    app.run(None)
