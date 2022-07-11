# Kantan

Configurable venv extension.

## How to use?

Kantan assumes the existence of a folder `~/.kantan` containing available configuration.

```
/~
    /.kantan
        /default
            configuration.json
            file_to_copy
```

Example `configuration.json`:

```
{
    "requirements: [ // Requirements to be installed using `pip install`
        numpy=1.2.3
    ],
    "include_files" : [ // Files to be copied to `env_dir`
        "file_to_copy"
    ]
}
```

Then as with `venv` a virtual environment can be created:

```
$ python -m kantan .venv [--config-name CONFIG_NAME=default]
```

## Development

### Python virtual environment

Create and load a virtual environement.

```
$ python -m venv .venv
$ source .venv/bin/activate
```

Install dependencies.

```
$ pip install -e '.[dev,pub]'
```

### Run tests, linter, bandit, black and isort

Running Pytest on the codebase.

```
$ python -m pytest .
```

Running Pylint on the codebase.

```
$ python -m pylint src
```

Running Bandit on the codebase.

```
$ python -m bandit -c pyproject.toml -r src
```

Running Black formatter on the codebase.

```
$ python -m black src
```

Running Isort formatter on the codebase.

```
$ python -m isort src
```

### Publish package

Build package.

```
$ python -m build .
```

Verify package.

```
$ python -m twine check dist/*
```

Upload package to a `pypi`.

```
$ python -m twine upload dist/*
```
