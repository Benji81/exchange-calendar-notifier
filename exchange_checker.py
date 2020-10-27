"""
CLI and Exchange checker functions
"""
from configparser import ConfigParser
from datetime import timedelta
from getpass import getpass
import os
from pathlib import Path
import time

from exchangelib import UTC_NOW, Account, Credentials
import keyring
from notifypy import Notify


INI_FILENAME = ".exchange-notifier.ini"
DEFAULT_CHECK_PERIOD_IN_MINUTES = 1


def notify(title="Event", message=None, location=None):
    """Send a system notification"""
    notification = Notify()
    notification.title = title
    notification.message = message
    if location:
        message += f"\nLocation: {location}"
    notification.icon = "./schedule.png"
    notification.audio = "./Polite.wav"
    notification.send()


class Checker:
    """Manage connection with Exchange and deals with calendar events"""

    def __init__(self, username: str, password: str, address: str = None) -> None:
        self.next_events = []
        self.already_notified = set()
        credentials = Credentials(username, password)
        if address is None:
            address = username
        self.account = Account(address, credentials=credentials, autodiscover=True)

    def store_next_events(self):
        """
        Get next events interesting fields. Next = between now and 1 day
        """
        self.next_events = [
            {
                "subject": item.subject,
                "start": item.start,
                "location": item.location,
                "remaining": item.start - UTC_NOW(),
                "sensitive": item.sensitivity in {"Private", "Confidential"},
                "sensitivity": item.sensitivity,
                "id": item.id,
            }
            # pylint: disable=no-member
            for item in self.account.calendar.filter(start__gt=UTC_NOW())
            .filter(start__lt=UTC_NOW() + timedelta(days=1))
            .order_by("start")
        ]

    def print_next_events(self):
        """debugging function"""
        for event in self.next_events:
            remaining = event["remaining"]
            print(remaining.seconds // 3600, (remaining.seconds % 3600) // 60)
            print(event, event["remaining"])

    def notify_if_in_less(self, seconds=0, minutes=10, hours=0, hide_sensitive=True):
        """Send notification if event will occurs before given time and is note sensitive"""
        for event in self.next_events:
            in_seconds = event["remaining"].seconds
            if (
                hide_sensitive
                and event["sensitive"]
                or event["id"] in self.already_notified
            ):
                continue
            if (
                in_seconds <= seconds
                or in_seconds // 60 < minutes
                or in_seconds // 3600 < hours
            ):
                notify(message=event["subject"], location=event["location"])
                self.already_notified.add(event["id"])


def get_conf():
    """
    Get conf from .ini file if exists or ask it with prompt and store it.
    Get password from keyring or ask and store it
    """
    path = os.path.join(str(Path.home()), INI_FILENAME)
    config = ConfigParser()
    if os.path.exists(path):
        config.read(path)
        username = config["DEFAULT"]["username"]
        address = config["DEFAULT"]["address"]
    else:
        print("Configuration not found")
        username = input("Enter username: ")  # nosec
        address = input("Enter address: ")  # nosec
        config["DEFAULT"]["username"] = username
        config["DEFAULT"]["address"] = address
        with open(path, "w") as configfile:
            config.write(configfile)

    password = keyring.get_password("exchange-notifier", username)
    if password is None:
        password = getpass("Enter password (will be store in keyring): ")
        keyring.set_password("exchange-notifier", username, password)

    return username, password, address


def main():
    """ main with an infinite loop"""
    username, password, address = get_conf()
    checker = Checker(username, password, address)
    while True:
        checker.store_next_events()
        checker.print_next_events()
        checker.notify_if_in_less(hours=20)
        time.sleep(60 * DEFAULT_CHECK_PERIOD_IN_MINUTES)


if __name__ == "__main__":
    main()
