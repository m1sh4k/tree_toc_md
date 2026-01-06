## Building & Installation

### Build uisng poetry
```bash
make build
make install # or make breaking-install
```

### Install via pip
Check out `.whl` file in releases section and install with
```bash
pip install /path/to/package.whl
```


## Usage

```
Usage: python toc_gen.py <directory> [-e] [-o|-g]
```
_\<directory\> must be a first argument_

### Flags description

- `-h` — help message
- `-e` _(optional)_ — add H1 heading below the filenames
- `-o` — make links to files in Obsidian (Wikilinks) format
- `-g` — make links to files in Github format (url encoded) (default)


## Makefile commands

- `make install` — install package uisng `poetry`
- `make build` — build package
- `make package-install` — install package to env using `pip`
- `make breaking-install` — install package to env breaking system packages using `pip`
- `make lint` — lint check with `ruff`
- `make lint-fix` — lint check with `ruff` using `--fix` option
