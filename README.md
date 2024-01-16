<h1 align="center">
lykos
</h1>
<p align="center">
  <a href="https://github.com/m1stadev/lykos/blob/master/LICENSE">
    <image src="https://img.shields.io/github/license/m1stadev/lykos">
  </a>
  <a href="https://github.com/m1stadev/lykos">
    <image src="https://tokei.rs/b1/github/m1stadev/lykos?category=code&lang=python&style=flat">
  </a>
  <a href="https://github.com/m1stadev/lykos/stargazers">
    <image src="https://img.shields.io/github/stars/m1stadev/lykos">
  </a>
</p>
A Python library/CLI tool for fetching *OS firmware keys.

Utilizes [The Apple Wiki](https://theapplewiki.com) as a source.

## Usage
```
Usage: lykos [OPTIONS]

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
- Python 3.8 or higher

## Installation
- Local installation:
    - `./install.sh`
    - Requires [Poetry](https://python-poetry.org)

## TODO
- Write documentation
- Push to PyPI

## Support
For any questions/issues you have, [open an issue](https://github.com/m1stadev/lykos/issues).