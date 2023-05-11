# monca-py
Bayesian AB testing in Python using the Monca Go API

## Getting started

### Clone this repo, and `cd` to it
```sh
git clone git@github.com:kasekun/monca-py.git
cd monca-py
```

### Install pipenv environment
```sh
pipenv --python 3.10.10
pipenv install
```

### Run the comparison
```sh
pipenv run python main.py
```

## Optional Setup

Automatically activate `pipenv` virtual environment in this directory and it's children

### install [direnv]('https://direnv.net/')

#### MacOS
```sh
brew install direnv
```

### allow `direnv`
this will target the `.envrc` file
```sh
direnv allow
```

### check python path is set correctly
```sh
which python
```
> `path/to/virtualenvs/monca-py-HASH/bin/python`
