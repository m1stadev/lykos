<h1 align="center">
plykos
</h1>
<p align="center">
  <a href="https://github.com/m1stadev/plykos/blob/master/LICENSE">
    <image src="https://img.shields.io/github/license/m1stadev/plykos">
  </a>
  <a href="https://github.com/m1stadev/plykos">
    <image src="https://tokei.rs/b1/github/m1stadev/plykos?category=code&lang=python&style=flat">
  </a>
  <a href="https://github.com/m1stadev/plykos/stargazers">
    <image src="https://img.shields.io/github/stars/m1stadev/plykos">
  </a>
</p>
A Python library/CLI tool for fetching *OS firmware keys.

Utilizes [The Apple Wiki](https://theapplewiki.com) as a source.

## Usage
```
Usage: plykos [OPTIONS]

  A Python CLI tool for fetching *OS firmware keys.

Options:
  --version                     Show the version and exit.
  -d, --device-identifier TEXT  Device identifier.  [required]
  -b, --build-id TEXT           *OS buildid.  [required]
  -c, --codename TEXT           *OS codename.
  -n, --component TEXT          Component to print keys for.
  -v, --verbose                 Enable verbose logging.
  -h, --help                    Show this message and exit.
```

## Requirements
- Python 3.10 or higher

## Installation
- Local installation:
    - `./install.sh`

## TODO
- Write documentation
- Push to PyPI

## Support
For any questions/issues you have, [open an issue](https://github.com/m1stadev/plykos/issues).