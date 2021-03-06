# Exchange calendar notifier

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
 <a href="https://github.com/psf/Benji81/exchange-calendar-notifier"><img alt="Actions Status" src="https://github.com/Benji81/exchange-calendar-notifier/workflows/CI/badge.svg"></a>
 <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

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
 