# lmc-runner
Run LMC assembly code from the command line.

## Installation
Using **pip**:
```console
$ pip install lmc-runner
```

## Usage
### Help
```console
$ lmc-runner -h

lmc-runner [-h] name

positional arguments:
  name        LMC assembly code file name

optional arguments:
  -h, --help  show this help message and exit
```
### Run LMC file
```console
$ lmc-runner [name]
```
Example from inside directory with file named `example.s`
```console
$ lmc-runner example.s
```
