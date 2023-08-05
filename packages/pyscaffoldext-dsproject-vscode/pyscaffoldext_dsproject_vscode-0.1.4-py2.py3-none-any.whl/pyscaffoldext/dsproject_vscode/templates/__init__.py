# -*- coding: utf-8 -*-
import os
import string
from pkg_resources import resource_string

from .. import __version__ as dsproject_version


def get_template(name):
    """Retrieve the template by name

    Args:
        name: name of template

    Returns:
        :obj:`string.Template`: template
    """
    file_name = "{name}.template".format(name=name)
    data = resource_string(__name__, file_name)
    # we assure that line endings are converted to '\n' for all OS
    data = data.decode(encoding="utf-8").replace(os.linesep, "\n")
    return string.Template(data)


def gitignore_all(opts):
    """gitignore file that ignores just everything

    Ignore everything except of this gitignore file.

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("gitignore_all")
    return template.safe_substitute(opts)


def gitignore_data(opts):
    """gitignore file that ignores almost everything

    Ignore everything except of gitignore also in sub directories.

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("gitignore_data")
    return template.safe_substitute(opts)


def gitkeep(opts):
    """.gitkeep file that keeps directory

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("gitkeep")
    return template.safe_substitute(opts)


def readme_md(opts):
    """Adds a basic README.md

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("readme_md")
    opts["pkg"] = opts["package"].ljust(19)
    opts["dsproject_version"] = dsproject_version
    return template.safe_substitute(opts)


def template_ipynb(opts):
    """Adds a template Jupyter notebook

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("template_ipynb")
    return template.safe_substitute(opts)


def train_model_py(opts):
    """Adds a template python experiment

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("train_model_py")
    return template.safe_substitute(opts)


def devcontainer_json(opts):
    """devcontainer.json for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("devcontainer_json")
    return template.safe_substitute(opts)


def devcontainer_local_json(opts):
    """devcontainer.local.json for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("devcontainer_local_json")
    return template.safe_substitute(opts)


def devcontainer_remote_json(opts):
    """devcontainer.remote.json for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("devcontainer_remote_json")
    return template.safe_substitute(opts)


def docker_compose_yml(opts):
    """docker-compose.yml for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("docker_compose_yml")
    return template.safe_substitute(opts)


def docker_compose_remote_yml(opts):
    """docker-compose.remote.yml for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("docker_compose_remote_yml")
    return template.safe_substitute(opts)


def dockerfile_dev_base(opts):
    """Dockerfile.dev.base for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("dockerfile_dev_base")
    return template.safe_substitute(opts)


def environment_dev_yml(opts):
    """environment.dev.yml for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("environment_dev_yml")
    return template.safe_substitute(opts)


def environment_dev_base_yml(opts):
    """environment.dev.base.yml for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("environment_dev_base_yml")
    return template.safe_substitute(opts)


def path_env(opts):
    """path.env for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("path_env")
    return template.safe_substitute(opts)


def settings_json(opts):
    """settings.json for vscode

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: file content as string
    """
    template = get_template("settings_json")
    return template.safe_substitute(opts)
