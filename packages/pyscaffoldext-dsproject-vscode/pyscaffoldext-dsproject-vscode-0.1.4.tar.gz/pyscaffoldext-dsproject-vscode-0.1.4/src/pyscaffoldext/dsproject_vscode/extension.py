# -*- coding: utf-8 -*-
import argparse

from pyscaffold.api import Extension, helpers
from pyscaffold.extensions.no_skeleton import NoSkeleton
from pyscaffold.extensions.pre_commit import PreCommit

from pyscaffoldext.markdown.extension import MarkDown

from . import templates


class IncludeExtensions(argparse.Action):
    """Activate other extensions
    """

    def __call__(self, parser, namespace, values, option_string=None):
        extensions = [
            NoSkeleton("no_skeleton"),
            PreCommit("pre_commit"),
            DSProjectVSCode("dsproject_vscode"),
        ]
        namespace.extensions.extend(extensions)


class DSProjectVSCode(Extension):
    """Template for data-science projects with support for VS Code container development
    """

    def augment_cli(self, parser):
        """Augments the command-line interface parser

        A command line argument ``--FLAG`` where FLAG=``self.name`` is added
        which appends ``self.activate`` to the list of extensions. As help
        text the docstring of the extension class is used.
        In most cases this method does not need to be overwritten.

        Args:
            parser: current parser object
        """
        help = self.__doc__[0].lower() + self.__doc__[1:]

        parser.add_argument(
            self.flag, help=help, nargs=0, dest="extensions", action=IncludeExtensions
        )
        return self

    def activate(self, actions):
        actions = self.register(actions, add_dsproject_vscode, after="define_structure")
        actions = self.register(actions, replace_readme, after="add_dsproject_vscode")
        return actions


def add_dsproject_vscode(struct, opts):
    """Adds basic module for custom extension

    Args:
        struct (dict): project representation as (possibly) nested
            :obj:`dict`.
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        struct, opts: updated project representation and options
    """
    gitignore_all = templates.gitignore_all(opts)
    gitkeep = templates.gitkeep(opts)

    path = [opts["project"], "data", ".gitignore"]
    struct = helpers.ensure(
        struct, path, templates.gitignore_data(opts), helpers.NO_OVERWRITE
    )
    for folder in ("external", "interim", "preprocessed", "raw"):
        path = [opts["project"], "data", folder, ".gitignore"]
        struct = helpers.ensure(struct, path, gitignore_all, helpers.NO_OVERWRITE)

    path = [opts["project"], "data", "output", ".gitkeep"]
    struct = helpers.ensure(struct, path, gitkeep, helpers.NO_OVERWRITE)

    path = [opts["project"], "notebooks", "template.ipynb"]
    template_ipynb = templates.template_ipynb(opts)
    struct = helpers.ensure(struct, path, template_ipynb, helpers.NO_OVERWRITE)

    path = [opts["project"], "scripts", "train_model.py"]
    train_model_py = templates.train_model_py(opts)
    struct = helpers.ensure(struct, path, train_model_py, helpers.NO_OVERWRITE)

    path = [opts["project"], "models", ".gitignore"]
    struct = helpers.ensure(struct, path, gitignore_all, helpers.NO_OVERWRITE)

    path = [opts["project"], "references", ".gitignore"]
    struct = helpers.ensure(struct, path, "", helpers.NO_OVERWRITE)

    path = [opts["project"], "reports", "figures", ".gitignore"]
    struct = helpers.ensure(struct, path, "", helpers.NO_OVERWRITE)

    # path = [opts["project"], ".devcontainer", "devcontainer.json"]
    # devcontainer_json = templates.devcontainer_json(opts)
    # struct = helpers.ensure(struct, path, devcontainer_json, helpers.NO_OVERWRITE)

    path = [opts["project"], ".devcontainer", "devcontainer.local.json"]
    devcontainer_local_json = templates.devcontainer_local_json(opts)
    struct = helpers.ensure(struct, path, devcontainer_local_json, helpers.NO_OVERWRITE)

    path = [opts["project"], ".devcontainer", "devcontainer.remote.json"]
    devcontainer_remote_json = templates.devcontainer_remote_json(opts)
    struct = helpers.ensure(struct, path, devcontainer_remote_json, helpers.NO_OVERWRITE)

    path = [opts["project"], ".devcontainer", "Dockerfile.dev.base"]
    dockerfile_dev_base = templates.dockerfile_dev_base(opts)
    struct = helpers.ensure(struct, path, dockerfile_dev_base, helpers.NO_OVERWRITE)

    path = [opts["project"], ".vscode", "settings.json"]
    settings_json = templates.settings_json(opts)
    struct = helpers.ensure(struct, path, settings_json, helpers.NO_OVERWRITE)

    path = [opts["project"], "environment.dev.base.yml"]
    environment_dev_base_yml = templates.environment_dev_base_yml(opts)
    struct = helpers.ensure(struct, path, environment_dev_base_yml, helpers.NO_OVERWRITE)

    path = [opts["project"], "docker-compose.yml"]
    docker_compose_yml = templates.docker_compose_yml(opts)
    struct = helpers.ensure(struct, path, docker_compose_yml, helpers.NO_OVERWRITE)

    path = [opts["project"], "docker-compose.remote.yml"]
    docker_compose_remote_yml = templates.docker_compose_remote_yml(opts)
    struct = helpers.ensure(struct, path, docker_compose_remote_yml, helpers.NO_OVERWRITE)

    path = [opts["project"], "path.env"]
    path_env = templates.path_env(opts)
    struct = helpers.ensure(struct, path, path_env, helpers.NO_OVERWRITE)

    path = [opts["project"], "requirements.txt"]
    struct = helpers.reject(struct, path)

    path = [opts["project"], "configs", ".gitignore"]
    struct = helpers.ensure(struct, path, "", helpers.NO_OVERWRITE)
    return struct, opts


def replace_readme(struct, opts):
    """Replace the readme.md of the markdown extension by our own

    Args:
        struct (dict): project representation as (possibly) nested
            :obj:`dict`.
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        struct, opts: updated project representation and options
    """
    # let the markdown extension do its job first
    struct, opts = MarkDown("markdown").markdown(struct, opts)

    file_path = [opts["project"], "README.md"]
    struct = helpers.reject(struct, file_path)
    readme = templates.readme_md(opts)
    struct = helpers.ensure(struct, file_path, readme, helpers.NO_OVERWRITE)
    return struct, opts
