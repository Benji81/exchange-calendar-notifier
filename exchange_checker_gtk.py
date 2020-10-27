"""
GTK Exchange checker application
"""
import threading
import time

import gi


gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
# pylint: disable=wrong-import-position
from gi.repository import AppIndicator3 as appindicator, GLib, Gtk as gtk


def main():
    """Main gtk app"""
    indicator = appindicator.Indicator.new(
        "exchangeChecker", "calendar", appindicator.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    def create_menu():
        """Replace the app menu each time it is called"""
        menu = gtk.Menu()
        command_one = gtk.MenuItem("Check events")
        command_one.connect("activate", "event_pressed")
        menu.append(command_one)
        menu.append(gtk.SeparatorMenuItem())
        exittray = gtk.MenuItem("Exit")
        exittray.connect("activate", gtk_quit)
        menu.append(exittray)

        menu.show_all()
        indicator.set_menu(menu)

    def check_loop():
        """Thread look to check and call menu update"""
        while True:
            print("Check")
            GLib.idle_add(create_menu)
            time.sleep(1)

    thread = threading.Thread(target=check_loop)
    thread.daemon = True
    thread.start()
    gtk.main()


def event_pressed(_):
    """Called when event item is selected in the menu"""


def gtk_quit(_):
    """Quit the application"""
    gtk.main_quit()


if __name__ == "__main__":
    main()
