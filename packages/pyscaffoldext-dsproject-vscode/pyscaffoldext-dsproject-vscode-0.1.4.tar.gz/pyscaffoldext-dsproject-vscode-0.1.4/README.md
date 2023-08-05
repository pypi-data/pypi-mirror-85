[![Build Status](https://api.travis-ci.com/avsolatorio/pyscaffoldext-dsproject-vscode.svg?branch=master)](https://travis-ci.com/github/avsolatorio/pyscaffoldext-dsproject-vscode)
[![Coverage Status](https://coveralls.io/repos/github/avsolatorio/pyscaffoldext-dsproject-vscode/badge.svg?branch=master)](https://coveralls.io/github/avsolatorio/pyscaffoldext-dsproject-vscode?branch=master)
[![PyPI-Server](https://img.shields.io/pypi/v/pyscaffoldext-dsproject-vscode.svg)](https://pypi.org/project/pyscaffoldext-dsproject-vscode)

# pyscaffoldext-dsproject-vscode

This extension is forked from the awesome [PyScaffold DSProject](https://github.com/pyscaffold/pyscaffoldext-dsproject) extension.

This version of the extension extends the functionality by adding a scaffold component for using the VS Code container development integration.

To benefit from this setup, you must use VS Code with Python and Remote - Containers extensions installed. Docker should also be installed on the host machine.

## Usage

Just install this package with `pip install pyscaffoldext-dsproject-vscode`
and note that `putup -h` shows a new option `--dsproject-vscode`.
Creating a data science project with VS Code container development integration is then as easy as:

```
putup --dsproject-vscode my_ds_project
```

After the project is created, set the following softlinks from the project root:

```
ln -s path.env .env
```

If you want to develop locally, create this softlink:

```
ln -s .devcontainer/devcontainer.local.json .devcontainer/devcontainer.json
```

Alternatively, if you want to develop using a remote docker server, use this:

```
ln -s .devcontainer/devcontainer.remote.json .devcontainer/devcontainer.json
```

If you have an application that will run inside the dev container that requires a port, specify the list of ports under the `forwardPorts` attribute in the following files:

```
.devcontainer/devcontainer.local.json
.devcontainer/devcontainer.remote.json
```

## Remote docker server

To use a remote docker server, specify the `docker.host` attribute in the `.vscode/settings.json` following the template in the file.

Edit the value of the `REMOTE_PATH` attribute in the `.env` file with the absolute path of the project in the remote server.

----------------------------

# pyscaffoldext-dsproject

[PyScaffold] extension tailored for *Data Science* projects. This extension is inspired by
[cookiecutter-data-science] and enhanced in many ways. The main differences are that it
1. advocates a proper Python package structure that can be shipped and distributed,
2. uses a [conda] environment instead of something [virtualenv]-based and is thus more suitable
   for data science projects,
3. more default configurations for [Sphinx], [py.test], [pre-commit], etc. to foster
   clean coding and best practices.

Also consider using [dvc] to version control and share your data within your team.
Read [this blogpost] to learn how to work with JupyterLab notebooks efficiently by using a
data science project structure like this.

The final directory structure looks like:
```
├── AUTHORS.rst             <- List of developers and maintainers.
├── CHANGELOG.rst           <- Changelog to keep track of new features and fixes.
├── LICENSE.txt             <- License as chosen on the command-line.
├── README.md               <- The top-level README for developers.
├── configs                 <- Directory for configurations of model & application.
├── data
│   ├── external            <- Data from third party sources.
│   ├── interim             <- Intermediate data that has been transformed.
│   ├── processed           <- The final, canonical data sets for modeling.
│   └── raw                 <- The original, immutable data dump.
├── docs                    <- Directory for Sphinx documentation in rst or md.
├── environment.yaml        <- The conda environment file for reproducibility.
├── models                  <- Trained and serialized models, model predictions,
│                              or model summaries.
├── notebooks               <- Jupyter notebooks. Naming convention is a number (for
│                              ordering), the creator's initials and a description,
│                              e.g. `1.0-fw-initial-data-exploration`.
├── references              <- Data dictionaries, manuals, and all other materials.
├── reports                 <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures             <- Generated plots and figures for reports.
├── scripts                 <- Analysis and production scripts which import the
│                              actual PYTHON_PKG, e.g. train_model.
├── setup.cfg               <- Declarative configuration of your project.
├── setup.py                <- Use `python setup.py develop` to install for development or
|                              or create a distribution with `python setup.py bdist_wheel`.
├── src
│   └── PYTHON_PKG          <- Actual Python package where the main functionality goes.
├── tests                   <- Unit tests which can be run with `py.test`.
├── .coveragerc             <- Configuration for coverage reports of unit tests.
├── .isort.cfg              <- Configuration for git hook that sorts imports.
└── .pre-commit-config.yaml <- Configuration of pre-commit git hooks.
```

See a demonstration of the initial project structure under [dsproject-demo] and also check out
the the documentation of [PyScaffold] for more information.


## Usage

Just install this package with `pip install pyscaffoldext-dsproject`
and note that `putup -h` shows a new option `--dsproject`.
Creating a data science project is then as easy as:
```
putup --dsproject my_ds_project
```

## Note

This project has been set up using PyScaffold 3.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.

[PyScaffold]: https://pyscaffold.org/
[cookiecutter-data-science]: https://github.com/drivendata/cookiecutter-data-science
[Miniconda]: https://docs.conda.io/en/latest/miniconda.html
[Jupyter]: https://jupyter.org/
[dsproject-demo]: https://github.com/pyscaffold/dsproject-demo
[Sphinx]: http://www.sphinx-doc.org/
[py.test]: https://docs.pytest.org/
[conda]: https://docs.conda.io/
[virtualenv]: https://virtualenv.pypa.io/
[pre-commit]: https://pre-commit.com/
[dvc]: https://dvc.org/
[this blogpost]: https://florianwilhelm.info/2018/11/working_efficiently_with_jupyter_lab/
