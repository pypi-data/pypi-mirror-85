## Booknot

![continuous_integration](https://github.com/FabienArcellier/booknot/workflows/continuous_integration/badge.svg)

Booknot helps you to take note about a webpage, a video on youtube or a pdf on the internet. It will create
a ready to use space to write note and reflexion using ``sphinx`` engine.

## Getting started

```bash
pip install booknot
```

## Usage

You should start from one of this configuration :

* start from scratch
* start from existing sphinx workspace

### start from scratch

1 . start your booknot project in an empty directory

``booknot init`` will propose you to create a sphinx workspace.

```text
$ booknot init
[?] This will bootstrap a workspace for sphinx in this directory, do you want to continue ? (y/N): y

[?] What the name of this booknot: Booknot
[?] What the name of the author: me

1. to render the booknot, use : make html
2. to open the booknot after rendering, use a browser and open _build/html/index.html
3. to bookmark a page, use : booknot capture https://...
```

2 . capture an existing page

```bash
booknot capture https://www.youtube.com/watch?v=q9T4tl1tmAY
```

### start from existing sphinx workspace

same workflow except booknot won't proposed to create a sphinx workspace. This pattern
allow to have more than one booknote by sphinx workspace.

```bash
# create a sphinx workspace by hand
sphinx-quickstart -p multibooknot -a me .

mkdir topic1
cd topic1
booknot init

cd ..
mkdir topic2
cd topic2
booknot init
```

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/booknot.git
```
## Developper guideline

### Add a dependency

Write the dependency in ``setup.py``. As it's the distribution standard for pypi,
I prefer to keep ``setup.py`` as single source of truth.

I encourage avoiding using instruction as ``pipenv install requests`` to register
a new library. You would have to write your dependency in both ``setup.py`` and ``Pipfile``.

### Install development environment

Use make to instanciate a python virtual environment in ./venv and install the
python dependencies.

```bash
make install_requirements_dev
```

### Update release dependencies

Use make to instanciate a python virtual environment in ./venv and freeze
dependencies version on requirement.txt.

```bash
make update_requirements
```

### Activate the python environment

When you setup the requirements, a `venv` directory on python 3 is created.
To activate the venv, you have to execute :

```bash
make venv
source venv/bin/activate
```

### Run the linter and the unit tests

Before commit or send a pull request, you have to execute `pylint` to check the syntax
of your code and run the unit tests to validate the behavior.

```bash
make lint
make tests
```

## Contributors

* Fabien Arcellier

## License

MIT License

Copyright (c) 2018 Fabien Arcellier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
