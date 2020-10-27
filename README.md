# Exchange calendar notifier
A small cli notifier for next events in your exchange calendar.

## Installation
For gtk version install necessary libraries
```bash
sudo apt install libgirepository1.0-dev libcairo2-dev gir1.2-appindicator3
```

Installation with pyenv and poetry:
```bash
pyenv local 3.8.1
poetry install
```

## Usage
For CLI version
```bash
poetry run python exchange-checker.py
```

For GTK version
```bash
poetry run python exchange-checker-gtk.py
```

## Information
* Store preferences in `$HOME/.exchange-notifier.ini`
* Store password in keyring

## Thanks:
 * sound from https://github.com/akx/Notifications
 * Icon made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com </a>
 