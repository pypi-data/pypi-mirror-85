[![PyPI](https://img.shields.io/pypi/v/horimote-mce.svg)](https://pypi.python.org/pypi/horimote-mce/)

# Hormiote-MCE

Listen for MCE remote button presses detected by [InputLIRC](https://packages.debian.org/buster/inputlirc) and send them to [horimote](https://github.com/benleb/horimote).

It is used to detect IR keypresses generated from a Windows MCE compatible remote (or a suitably configured Logitech Harmony Hub) and send them to a Samsung SMT-G7400/G7401 box, commonly branded as the Virgin Media/upc/Unitymedia Horizon box used by several European cable operators. This allows commands that cannot be sent via IR (eg. DVD, Guide button) to be emulated via the SMT-G7400/G7401 IP interface.

## Installation

This script should run on most Linux installations (including Raspbian/Rasperry Pi OS) and requires the following:

- an MCE IR receiver that is supported by inputlirc.
- `inputlirc` package installed on the underlying operating system
- `hormiote` package installed via `pip`
