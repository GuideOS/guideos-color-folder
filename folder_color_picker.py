#!/usr/bin/env python3
import sys
import os
import subprocess
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, Gio

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
    def __init__(self, app, target_path, all_targets):
        super().__init__(application=app, title="Ordnerfarbe (Mehrfachauswahl)")
        self.target_paths = all_targets
        self.target_path = os.path.abspath(target_path)

        self.set_default_size(240, 210)
        self.set_resizable(False)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        self.set_child(box)

        # Zeigt den Namen des ersten Ordners und optional die Anzahl an
        folder_name = os.path.basename(self.target_path)
        count_info = f" (+ {len(self.target_paths) - 1} weitere)" if len(self.target_paths) > 1 else ""
        label = Gtk.Label(label=f"<b>{folder_name}{count_info}</b>")
        label.set_use_markup(True)
        box.append(label)

        grid = Gtk.Grid()
        grid.set_column_spacing(6)
        grid.set_row_spacing(6)
        grid.set_halign(Gtk.Align.CENTER)
        box.append(grid)

        cols = 4
        for idx, (name, hex_code, icon_key) in enumerate(PALETTE):
            btn = Gtk.Button()
            btn.set_tooltip_text(name)
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

            btn.connect("clicked", self.on_color_selected, icon_key)
            grid.attach(btn, idx % cols, idx // cols, 1, 1)

        reset_btn = Gtk.Button(label="Standard zurücksetzen")
        reset_btn.set_margin_top(4)
        reset_btn.connect("clicked", self.on_reset_clicked)
        box.append(reset_btn)

    def apply_icon(self, icon_name):
        if icon_name:
            icon_path = None
            base_paths = [
                os.path.expanduser("~/.local/share/icons/Papirus"),
                "/usr/share/icons/Papirus",
                os.path.expanduser("~/.local/share/icons/papirus-icon-theme"),
                "/usr/share/icons/papirus-icon-theme"
            ]

            for base in base_paths:
                candidate = os.path.join(base, "64x64", "places", f"{icon_name}.svg")
                if os.path.exists(candidate):
                    icon_path = candidate
                    break
                candidate_alt = os.path.join(base, "48x48", "places", f"{icon_name}.svg")
                if os.path.exists(candidate_alt):
                    icon_path = candidate_alt
                    break

            # Schleife für alle ausgewählten Ordner
            for path in self.target_paths:
                if icon_path:
                    subprocess.run(["gio", "set", "-t", "string", path, "metadata::custom-icon", f"file://{icon_path}"], check=False)
                    subprocess.run(["gio", "set", "-t", "unset", path, "metadata::custom-icon-name"], check=False)
                else:
                    subprocess.run(["gio", "set", "-t", "string", path, "metadata::custom-icon-name", icon_name], check=False)
                subprocess.run(["touch", path], check=False)
        else:
            for path in self.target_paths:
                subprocess.run(["gio", "set", "-t", "unset", path, "metadata::custom-icon-name"], check=False)
                subprocess.run(["gio", "set", "-t", "unset", path, "metadata::custom-icon"], check=False)
                subprocess.run(["touch", path], check=False)

        self.close()

    def on_color_selected(self, button, icon_key):
        full_icon_name = f"folder-{icon_key}"
        self.apply_icon(full_icon_name)

    def on_reset_clicked(self, button):
        self.apply_icon(None)

class ColorPickerApp(Gtk.Application):
    def __init__(self, target_paths):
        super().__init__(application_id="org.nemo.foldercolorpicker")
        self.target_paths = target_paths

    def do_activate(self):
        win = ColorPickerWindow(self, self.target_paths[0], self.target_paths)
        win.present()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Fehler: Keine Pfade übergeben.")
        sys.exit(1)

    app = ColorPickerApp(sys.argv[1:])
    app.run(None)
