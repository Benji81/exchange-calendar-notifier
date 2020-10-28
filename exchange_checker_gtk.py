"""
GTK Exchange checker application
"""
import threading
import time

import gi
from tzlocal import get_localzone


gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
# pylint: disable=wrong-import-position
from gi.repository import AppIndicator3 as appindicator, GLib, Gtk as gtk

from exchange_checker import DEFAULT_CHECK_PERIOD_IN_MINUTES, Checker, get_conf


def main():
    """Main gtk app"""
    indicator = appindicator.Indicator.new(
        "exchangeChecker", "calendar", appindicator.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    def create_menu(with_event=True):
        """Replace the app menu each time it is called"""
        menu = gtk.Menu()
        command_one = gtk.MenuItem("Check now")
        command_one.connect("activate", check_now)
        menu.append(command_one)
        menu.append(gtk.SeparatorMenuItem())

        if with_event:
            checker.store_next_events()
            print("check_done")
            for event in checker.next_events:
                event_item = gtk.MenuItem(
                    f"{event['subject']}"
                    f" in {Checker.remaining_time_text(event)}"
                    f" at {event['start'].astimezone(get_localzone()).strftime('%H:%M')}"
                )
                event_item.connect("activate", event_pressed, event)
                menu.append(event_item)
                menu.append(gtk.SeparatorMenuItem())
        exittray = gtk.MenuItem("Exit")
        exittray.connect("activate", gtk_quit)
        menu.append(exittray)

        menu.show_all()
        indicator.set_menu(menu)

    def check_now(_):
        """Refresh events list"""
        print("check now")
        checker.store_next_events()
        print("check_done")

    def event_pressed(_, event):
        """Called when event item is selected in the menu"""
        dialog = gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=gtk.MessageType.INFO,
            buttons=gtk.ButtonsType.OK,
            text=f"{event['subject']}\n",
        )
        dialog.format_secondary_text(
            f"Location: {event['location']}\n\n"
            f"Start: {event['start'].astimezone(get_localzone()).strftime('%y-%m-%d %H:%M')}\n\n"
            f"Sensitivity: {event['sensitivity']}"
        )
        dialog.run()

        dialog.destroy()

    def check_loop():
        """Thread look to check and call menu update"""
        while True:
            print("Check")
            GLib.idle_add(create_menu)
            time.sleep(DEFAULT_CHECK_PERIOD_IN_MINUTES * 60)

    username, password, address = get_conf()
    checker = Checker(username, password, address)

    thread = threading.Thread(target=check_loop)
    thread.daemon = True
    thread.start()
    create_menu(with_event=False)
    gtk.main()


def gtk_quit(_):
    """Quit the application"""
    gtk.main_quit()


if __name__ == "__main__":
    main()
