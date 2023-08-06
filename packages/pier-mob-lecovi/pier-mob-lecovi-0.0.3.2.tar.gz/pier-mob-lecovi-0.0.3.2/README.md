# Sample Python CLI

Sample repository for creating a CLI in Python.

## Motivation

This repository is for educational purposes. I want to show how to create an executable 
CLI tool written in Python. With this I wanna cover:

- [x] Creating a Python Package using traditional `setup.py`.
- [ ] Creating a Python Package using `poetry`.
- [x] Publishing to PyPI.
- [x] Creating a simple CLI tool that installs on to your system and is executable.
- [ ] Creating plugins for the CLI tool that are *pipinstalable*.

# Package

We are going to create a package called `pier-mob`. Why? Just because! I don't wanna use
traditional `example`, `foo`, or `bar` because I think those names lack semantics
and the use of such names becomes difficult for less experienced devs to understand. If
you are wondering, I let [roke](https://github.com/ralsina/roke) choose the name for the 
example tool that we are going to build.

Add files and directories:

```baah
pier_mob
|-- LICENSE               # License file
|-- README.md             # **This** file
|-- pier_mob              # Main directory: all source code inside
|   |-- __init__.py       # needed for converting directory into a package
|   |-- __main__.py       # Defines what is executed when package is called
|   `-- cli.py            # Sample source code module
|-- setup.py              # Python Packaging config file
`-- tests                 # Test cases directory
    |-- __init__.py       # needed for converting directory into a package
    `-- test_version.py   # Test source code sample
```

With this minimal structure we can run our program as module and as a simple script.
Using [pip](https://github.com/pypa/pip/blob/master/src/pip/__main__.py) strategy to be
able of running in both ways. Look deeper on [`pier_mob/__main__.py`](./pier_mob/__main__.py).

As simple script:

```bash
$ python3 pier_mob
Pier Mob v0.0.1
```

And running as module:

```bash
$ python3 -m pier_mob
Pier Mob v0.0.1
```

Also with this minimal structure we have tests.

Tests can be run as:

```bash
$ python3 setup.py test
```

## Let's publish our package

You will need `setuptools`, `wheel`, and `twine` for creating and uploading to PyPI.
Install this packages with `pip` in new virtualenv or in your user level packages.

Create a new virualenv, activate it and install needed packages:

```bash
$ python3 -m venv pier_build
$ source pier_build/bin/activate
(pier_build) $ pip install setuptools wheel twine
```

Now we need to build source distribution files. Run the following command:

```bash
(pier_build) $ python3 setup.py sdist bdist_wheel
```
This command will output a lot of text and once completed will generate two files in the
`dist` directory: a `.tar.gz` which is a Source Distribution, and a `.whl` which is a 
Built Distribution.

Now we are ready to upload our package. Use your PyPI account and create a new API Token.
When `twine` prompts your username write `__token__` then use your API Token as password.

```bash
(pier_build) $ python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: __token__
Enter your password:
```

✨ 🍰 ✨ Congrats! Your package is now published on PyPI: https://pypi.org/project/pier-mob-lecovi/

Create a new virtualenv and install your package from PyPI

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install pier-mob-lecovi
...
$ python
```

Inside REPL run:

```python
>>> import pier_mob
>>> pier_mob.version()
'0.0.1'
```

✨ 🍰 ✨ It works!!

### Test PyPI

It's a complete separate instance. If you have a user on PyPI you need to create another
one for Test PyPI (and vivecersa). The same goes for Tokens.

- Upload URL: https://test.pypi.org/legacy/
- Pip download URL: https://test.pypi.org/simple/ (remember to add `--index-url`)

## Executable

Let's change [`pier_mob/__main__.py`](./pier_mob/__main__.py) for creating a console
script instalable. Wrap the `print` function inside `main()` and modify `setup.py`

```python
entry_points={
'console_scripts': [
    'pier=pier_mob.__main__:main',
    ],
},
```

This will create a `pier` executable that will call the `main()` function inside 
`__main__.py`.

Create a new virtualenv and test installation:

```bash
$ python3 -m venv executable
$ source executable/bin/activate
(executable) $ python3 setup.py install
(executable) $ pier
Pier Mob v0.0.2
```

## Adding commands

Let's improve our interface using [Typer](https://typer.tiangolo.com/). 
Add `info()` and `version()` functions to [cli.py](./pier_mob/cli.py). 
*DON'T FORGET TO UPDATE `__version__`*.
You also will need to update `__main__` and `__init__` and import the new `app` instead 
of `version()`.
We need to change our unittest for the better `pytest` suite. 

```bash
(install) $ pip install typer pytest
```

Now test must be run with:

```bash
(install) $ pytest
```

Now you can update your package on PyPI.

```bash
(build) $ python3 setup.py build
(build) $ python3 -m twine upload --repository pypi dist/*
```

# Resources

- [Packaging Python](https://packaging.python.org/tutorials/packaging-projects/)
- [How To Package Your Python Code](https://python-packaging.readthedocs.io/en/latest/index.html)
