# comexdown: Brazil's foreign trade data downloader

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dankkom/comexdown/tests?style=flat-square) ![Coveralls github](https://img.shields.io/coveralls/github/dankkom/comexdown?style=flat-square) ![GitHub](https://img.shields.io/github/license/dankkom/comexdown?style=flat-square) ![PyPI](https://img.shields.io/pypi/v/comexdown?style=flat-square)

This package contains functions to download brazilian foreign trade data
published by [Ministerio da Economia(ME)/Secretaria de Comercio Exterior (SCE)][1].

## Installation

`comexdown` package is available on PyPI, so just use `pip`!

```shell
pip install comexdown
```

## Usage

```python
import comexdown

# Download main NCM table in the directory ./DATA
comexdown.ncm(table="ncm", path="./DATA")

# Download 2019 exports data file in the directory ./DATA
comexdown.exp(year=2019, path="./DATA")
```

## Command line tool

Download data on Brazilian foreign trade transactions (Exports / Imports).

You can specify a range of years to download at once.

```
comexdown trade 2008:2019 -o "./DATA"
```

Download code tables.

```shell
comexdown table all       # Download all related code files
comexdown table uf        # Download only the UF.csv file
comexdown table ncm_cgce  # Download only the NCM_CGCE.csv file
comexdown table nbm_ncm   # Download only the NBM_NCM.csv file
```

## Development

To setup a development environment clone this repository and install the required packages:

```shell
git clone https://github.com/dankkom/comexdown.git
cd comexdown
pipenv install --dev  # Requires Python 3.9
```

### Run tests

To run the tests suite, use the following command:

```shell
pytest --cov=comexdown --cov-report term-missing --cov-report html tests/
```

[1]: http://www.mdic.gov.br/index.php/comercio-exterior/estatisticas-de-comercio-exterior/base-de-dados-do-comercio-exterior-brasileiro-arquivos-para-download
