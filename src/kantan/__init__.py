import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import venv

logger = logging.getLogger(__name__)


class KantanEnvBuilder(venv.EnvBuilder):
    def __init__(self, *args, **kwargs):
        config_name = kwargs.pop("config_name", "default")
        user_home = os.path.expanduser("~")
        self.config_dir_path = os.path.join(user_home, ".kantan", config_name)

        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        TODO: Add description

        :param context: The information for the environment creation request
                        being processed.
        """

        print(self.config_dir_path)

        if os.path.exists(self.config_dir_path):
            config_file_path = os.path.join(self.config_dir_path, "configuration.json")

            print(config_file_path)

            if os.path.isfile(config_file_path):
                with open(config_file_path, "r", encoding="utf8") as config_file:
                    config = json.load(config_file)

                    if "requirements" in config:
                        for package_ref in config["requirements"]:
                            self.install_dependency(context, package_ref)

                    if "include_files" in config:
                        for file_path in config["include_files"]:
                            self.copy_file_to_env_dir(context, file_path)

    def install_dependency(self, context, package_ref):
        logger.debug("Installing %s package in %s", package_ref, context.bin_path)
        cmd = [context.env_exec_cmd, "-m", "pip", "install"]
        cmd.append(package_ref)
        subprocess.check_call(cmd)

    def copy_file_to_env_dir(self, context, file_path):
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.config_dir_path, file_path)
        file_dir, file_name = os.path.split(file_path)
        dst_path = os.path.join(context.env_dir, file_name)

        print(file_path, file_name, file_dir, dst_path)

        logger.debug("Copying %s from %s to %s", file_name, file_dir, context.env_dir)
        shutil.copyfile(file_path, dst_path)


def create(
    env_dir,
    system_site_packages=False,
    clear=False,
    symlinks=False,
    with_pip=False,
    prompt=None,
    upgrade_deps=False,
    config_name="default",
):
    """Create a virtual environment in a directory."""
    builder = KantanEnvBuilder(
        system_site_packages=system_site_packages,
        clear=clear,
        symlinks=symlinks,
        with_pip=with_pip,
        prompt=prompt,
        upgrade_deps=upgrade_deps,
        config_name=config_name,
    )
    builder.create(env_dir)


def main(args=None):
    if sys.version_info < (3, 3) or not hasattr(sys, "base_prefix"):
        raise ValueError("This script is only for use with Python >= 3.3")

    parser = argparse.ArgumentParser(
        prog=__name__,
        description="Creates virtual Python "
        "environments in one or "
        "more target "
        "directories.",
        epilog="Once an environment has been "
        "created, you may wish to "
        "activate it, e.g. by "
        "sourcing an activate script "
        "in its bin directory.",
    )
    parser.add_argument(
        "dirs",
        metavar="ENV_DIR",
        nargs="+",
        help="A directory to create the environment in.",
    )
    parser.add_argument(
        "--system-site-packages",
        default=False,
        action="store_true",
        dest="system_site",
        help="Give the virtual environment access to the " "system site-packages dir.",
    )
    if os.name == "nt":
        use_symlinks = False
    else:
        use_symlinks = True
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--symlinks",
        default=use_symlinks,
        action="store_true",
        dest="symlinks",
        help="Try to use symlinks rather than copies, "
        "when symlinks are not the default for "
        "the platform.",
    )
    group.add_argument(
        "--copies",
        default=not use_symlinks,
        action="store_false",
        dest="symlinks",
        help="Try to use copies rather than symlinks, "
        "even when symlinks are the default for "
        "the platform.",
    )
    parser.add_argument(
        "--clear",
        default=False,
        action="store_true",
        dest="clear",
        help="Delete the contents of the "
        "environment directory if it "
        "already exists, before "
        "environment creation.",
    )
    parser.add_argument(
        "--upgrade",
        default=False,
        action="store_true",
        dest="upgrade",
        help="Upgrade the environment "
        "directory to use this version "
        "of Python, assuming Python "
        "has been upgraded in-place.",
    )
    parser.add_argument(
        "--without-pip",
        dest="with_pip",
        default=True,
        action="store_false",
        help="Skips installing or upgrading pip in the "
        "virtual environment (pip is bootstrapped "
        "by default)",
    )
    parser.add_argument(
        "--prompt",
        help="Provides an alternative prompt prefix for " "this environment.",
    )
    parser.add_argument(
        "--upgrade-deps",
        default=False,
        action="store_true",
        dest="upgrade_deps",
        help=f"Upgrade core dependencies: {venv.CORE_VENV_DEPS} to the latest version in PyPI",
    )
    parser.add_argument(
        "--config-name",
        default="default",
        help=f"Upgrade core dependencies: {venv.CORE_VENV_DEPS} to the latest version in PyPI",
    )
    options = parser.parse_args(args)
    if options.upgrade and options.clear:
        raise ValueError("you cannot supply --upgrade and --clear together.")
    builder = KantanEnvBuilder(
        system_site_packages=options.system_site,
        clear=options.clear,
        symlinks=options.symlinks,
        upgrade=options.upgrade,
        with_pip=options.with_pip,
        prompt=options.prompt,
        upgrade_deps=options.upgrade_deps,
        config_name=options.config_name,
    )
    for directory in options.dirs:
        builder.create(directory)


def raw_main():
    return_code = 1
    try:
        main()
        return_code = 0
    except Exception as exception:
        print(f"Error: {exception}", file=sys.stderr)
    sys.exit(return_code)


if __name__ == "__main__":
    raw_main()
