# Command Line Client in Python with Click

Click is a utility to assist in the creation fo command line tools. With simple annotations you can easily execute functions and automatically parse input parameters. Help documentation is built in and easy to augment. 

In addition to the features provided by click, I'll also be reviewing setuptools and some path constructs to mange the project better. 

In this repo we'll cover the following concepts:

- Your First Command
- Switching to setuptools
- Command Groups
- Breaking out into separate files


## Your first command

Click is very easy to get started. Let's use `virtualenv` to keep things tidy. 

```
    $ virtualenv venv
    $ source venv/bin/activate
```

Now install click

```
    $ pip install click
```

Now for the code
`main.py`
```
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """ Greeting all worthy coders """
    for x in range(count):
        click.echo('Hello %s!' % name)

if __name__ == '__main__':
    hello()
```

We can now get help insights on our stack

```
$ python hiho.py --help
Usage: hiho.py [OPTIONS]

  Greeting all worthy coders

Options:
  --count INTEGER  Number of greetings.
  --name TEXT      The person to greet.
  --help           Show this message and exit.
  ```

And calling with params will execute the function and prompt for input

```
$ python hiho.py
Your name:
```

```
# python hiho.py
Your name: Chris
Hello Chris!
```

Thats interesting but lets make this more realistic

## Setuptools
First off fo a good commandline tool we wouldn't be calling `python` or specifying the file `hiho.py` Instead we want an executable wrapper we can call directly. Enter setuptools

It's pretty easy to use, just start with a setup.py in your root directory

`setup.py`
```
from setuptools import setup, find_packages

setup(
    name='myscript',
    version='0.1',
    py_modules=['hiho'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hey=hello:hello
    ''',
)

```

nothing scary:
- name: whatever you want to call it
- version: yep just a version
- py_modules: modules to load (will make it more robust soon)
- install_requires: any required libraries you need
- entry_points: the magic. create a console script called `hey` and use the hello method from the hello module as the main etry point


## Grouping commands

You'll most likely want to structure your commands to be more easily accessed. Click supports grouping commands so you can call `$ yourscript parent_command child_command`

Heres an example

```

import click

@click.group()
def mybase(debug):
    click.echo('Base')
    pass

@mybase.command()
def sync():
    click.echo('Synching')

```

````
$ yourscript sync
Base
Synching

```

## Breaking out into separate files

I'm sure there are multiple ways to do this. After messing with this for a bit I landed on initializing click in the `__init__.py` file

`myapp/__init__.py`
```

import click


@click.group()
def cli():
    pass

from myapp import main
from myapp import othercommands

```

Then in the modules themselves we import the package to extend the commands

```

import click
from myapp import cli

@cli.command()
def somecommand():
    click.echo("hello there")

```
