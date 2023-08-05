# Block utilities package

## Install
Create a virtual env:
```bash
mkvirtualenv up42-blockutils --python=$(which python3.7)
```
Install the package with system link:
```
pip install -e libs/python3
pip install -r libs/python3/requirements-docs.txt --use-feature=2020-resolver
```

## Deploy manually to PyPi

Make use you have `PYPI_USER` and `PYPI_PASSWORD` set in your environment.

Update the version of the package in [_version.txt](blockutils/_version.txt).

```bash
make update-blockutils
```

## Update documentation

Serve documentation locally:
```bash
mkdocs serve -f libs/python3/mkdocs.yml
```

Update documentation:
```bash
make update-docs-blockutils
```
