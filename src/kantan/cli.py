import argparse
import os
import sys
import venv

from kantan import builder


def run(args=None):
    if sys.version_info < (3, 7) or not hasattr(sys, "base_prefix"):
        raise ValueError("This script is only for use with Python >= 3.7")

    if sys.version_info[:2] < (3, 9):
        if not hasattr(venv, "CORE_VENV_DEPS"):
            venv.CORE_VENV_DEPS = ('pip', 'setuptools') # type: ignore

    parser = argparse.ArgumentParser(
        prog="kantan",
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
        "by default).",
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
        help=f"Upgrade core dependencies: {venv.CORE_VENV_DEPS} to the latest version in PyPI.", # type: ignore
    )
    parser.add_argument(
        "--config-name",
        default="default",
        help="Target configuration to load from `$HOME/.kantan'.",
    )
    options = parser.parse_args(args)
    if options.upgrade and options.clear:
        raise ValueError("you cannot supply --upgrade and --clear together.")

    for directory in options.dirs:
        builder.create(
            directory,
            system_site_packages=options.system_site,
            clear=options.clear,
            symlinks=options.symlinks,
            upgrade=options.upgrade,
            with_pip=options.with_pip,
            prompt=options.prompt,
            upgrade_deps=options.upgrade_deps,
            config_name=options.config_name,
        )


def main():
    return_code = 1
    try:
        run()
        return_code = 0
    except Exception as exception:  # pylint: disable=W0703
        print(f"Error: {exception}", file=sys.stderr)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
