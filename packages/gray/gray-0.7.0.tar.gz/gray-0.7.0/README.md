# gray

[![Package Version](https://badge.fury.io/py/gray.svg)](http://badge.fury.io/py/gray)
[![Build Status](https://travis-ci.org/dizballanze/gray.svg?branch=master)](https://travis-ci.org/dizballanze/gray)

Less uncompromising Python code formatter.

Gray stands on the shoulders of giants:

- [isort](https://timothycrosley.github.io/isort/) - imports sorting and more
- [pyupgrade](https://github.com/asottile/pyupgrade) - automatically upgrades syntax for newer versions of Python
- [autoflake](https://github.com/myint/autoflake) - remove unused imports and variables
- [add-trailing-comma](https://github.com/asottile/add-trailing-comma)
- [trim](https://github.com/myint/trim) - remove trailing whitespaces
- [unify](https://github.com/myint/unify) - unify quotes style


## Usage

```
usage:
        gray myapp.py
        gray myproj/ tests/
        gray --log-level debug --formatters isort,unify ~/app


Less uncompromising Python code formatter. Args that start with '--' (eg.
--pool-size) can also be set in a config file (/Users/dizballanze/.gray or
/etc/gray.conf or ./gray.conf). Config file syntax allows: key=value,
flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi).
If an arg is specified in more than one place, then commandline values
override config file values which override defaults.

positional arguments:
  paths                 Paths to format (default: (PosixPath('.'),))

optional arguments:
  -h, --help            show this help message and exit
  --pool-size POOL_SIZE
                        process pool size (default: 8)
  --do-not-detect-venv  Don't try to detect virtualenv (default: False)

Logging options:
  --log-level {debug,info,warning,error,fatal}
  --log-format {stream,color,json,syslog}

Formatters options:
  -f FORMATTERS, --formatters FORMATTERS
                        Enabled formatters separated by comma (default: add-
                        trailing-comma,autoflake,isort,pyupgrade,trim,unify)
  --min-python-version MIN_PYTHON_VERSION
                        Minimum python version to support (default: (3, 7))

pyupgrade options:
  --pyupgrade-keep-percent-format
                        Do not upgrade percent formatted strings to f-strings
                        (default: False)

unify options:
  --unify-quote UNIFY_QUOTE
                        preferred quote (default: ")

isort options:
  --isort-line-length ISORT_LINE_LENGTH
                        isort section (default: 80)
  --isort-virtual-env ISORT_VIRTUAL_ENV
                        virtual env path (default:
                        /Users/dizballanze/apps/gray/env)
  --isort-include-trailing-comma ISORT_INCLUDE_TRAILING_COMMA
                        include a trailing comma on multi line imports
                        (default: 1)
  --isort-lines-after-imports ISORT_LINES_AFTER_IMPORTS
                        empty lines after imports (default: 2)

autoflake options:
  --autoflake-ignore-init-module-imports AUTOFLAKE_IGNORE_INIT_MODULE_IMPORTS
  --autoflake-expand-star-imports AUTOFLAKE_EXPAND_STAR_IMPORTS
  --autoflake-remove-all-unused-imports AUTOFLAKE_REMOVE_ALL_UNUSED_IMPORTS
  --autoflake-remove-duplicate-keys AUTOFLAKE_REMOVE_DUPLICATE_KEYS
  --autoflake-remove-unused-variables AUTOFLAKE_REMOVE_UNUSED_VARIABLES

trim options:
  --trim-leading-newlines TRIM_LEADING_NEWLINES
```


## Git Hook

You can setup gray formatting before each commit with pre-commit git hook.
Add following file to `.git/hooks/pre-commit` and make it executable with
`chmod +x .git/hooks/pre-commit`.

```python
#!/usr/bin/env python
from gray.hooks import git_pre_commit

exit(git_pre_commit(stop_on_modify=True))
```

If `stop_on_modify` argument is `True`, hook will prevent commit if there are
any unstaged changes in files you about to commit.

Otherwise, any unstaged changes in this files will be added to the index
by the hook.


## Config file

Gray is looking for config file in `./gray.conf`, `/etc/gray.conf` or `~/.gray`.

Example of grayconf:

```
formatters = add-trailing-comma,isort,unify
min-python-version = 3.5
```

## Features

* TODO

## Git pre-commit hook

Use [pre-commit](https://pre-commit.com/). Once you
[have it installed](https://pre-commit.com/#install), add this to the
`.pre-commit-config.yaml` in your repository:

```yaml
repos:
  - repo: https://github.com/dizballanze/gray
    rev: master # Replace by any tag/branch: https://github.com/dizballanze/gray/tags
    hooks:
      - id: gray
```

and run `pre-commit install`.

## Using with Sourcetree
Sourcetree may run without `gray` being available via `PATH`.

### MacOS
Make sure `gray` is available via `PATH` and run `open /Applications/Sourcetree.app`.
Or better [create](https://stackoverflow.com/a/281455/1555653) an `Automator` workflow 
with `source ~/.bash_profile && open /Applications/Sourcetree.app` script.
