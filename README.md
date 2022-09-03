# Kantan

Configurable venv extension.

## How to use?

Kantan assumes the existence of a folder `$HOME/.kantan` containing available configuration.

```
/$HOME
    /.kantan
        /default
            configuration.json
            file_to_copy
```

Example `configuration.json`:

```
{
    "requirements": [ // Requirements to be installed on the new environment using `pip install`
        "numpy=1.2.3"
    ],
    "include_files" : [ // Files to be copied to `env_dir`
        "file_to_copy"
    ]
}
```

Then check how to use kantan from commandline.

```
$ kantan -h
```

## Development

### Python virtual environment

Create and load a virtual environement.

```
python -m venv .venv
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

## Areas of improvement

- Add/Test Support for older/newer Python versions.
- Json schema for `configuration.json` validation.
- Make configuration extendable.
- Improve coverage of builder and extensions.
- Improve error handling and messages
