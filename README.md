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
python -m kantan .venv
source .venv/bin/activate
```

### Install

Install all dependencies in editable mode.

```
make install
```

### Misc

Check what other shortcuts are available.

```
make help
```
