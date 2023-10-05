[![Python 3.6](https://img.shields.io/badge/Python3-%3E%3D3.6-blue)](https://www.python.org/downloads)

# VNCheck
VNCheck is a Python tool checking Helm value environments and syntax.

#
```bash
vncheck/
├── Dockerfile
├── LICENSE
├── newSchema.json
├── oldSchema.json
├── README.md
├── requirements.txt
├── VERSION
└── vncheck.py

0 directories, 8 files
```
#
## Requirements
```bash
pyyaml
cerberus
```
#
## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.
```bash
pip3 install -r requirements.txt
```
#
## Usage
```python
usage: vncheck.py [-h] [--check-env] [--check-schema] [--schema-directory SCHEMA_DIRECTORY] [--value-file VALUE_FILE] [--exclude EXCLUDE]

A tool to validate Helm value file

options:
  -h, --help                            show this help message and exit
  --check-env                           enable to check ENV variables in Helm value file
  --check-schema                        enable to check Helm value file based on schema
  --schema-directory SCHEMA_DIRECTORY   schema directory
  --value-file VALUE_FILE               path to a Helm value file
  --exclude EXCLUDE                     exclude files not needed to check

Author: _wiky
```
## License
[MIT](https://choosealicense.com/licenses/mit/)