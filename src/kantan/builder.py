import json
import logging
import os
import shutil
import subprocess
import sys
import venv
from types import SimpleNamespace

logger = logging.getLogger(__name__)


def create(  # pylint: disable=R0913
    env_dir,
    system_site_packages=False,
    clear=False,
    symlinks=False,
    upgrade=False,
    with_pip=False,
    prompt=None,
    upgrade_deps=False,
    config_name="default",
):
    """Create a virtual environment in a directory."""
    if sys.version_info[:2] < (3, 9):
        builder = KantanEnvBuilder(
            system_site_packages=system_site_packages,
            clear=clear,
            symlinks=symlinks,
            upgrade=upgrade,
            with_pip=with_pip,
            prompt=prompt,
            config_name=config_name,
        )
    else:
        builder = KantanEnvBuilder(
            system_site_packages=system_site_packages,
            clear=clear,
            symlinks=symlinks,
            upgrade=upgrade,
            with_pip=with_pip,
            prompt=prompt,
            upgrade_deps=upgrade_deps,
            config_name=config_name,
        )

    builder.create(env_dir)


class KantanEnvBuilder(venv.EnvBuilder):

    KANTAN_CONFIG_DIR = os.path.join("~", ".kantan")
    KANTAN_CONFIG_FILE = "configuration.json"

    def __init__(self, *args, **kwargs):
        config_name = kwargs.pop("config_name", "default")
        kantan_home = os.path.expanduser(self.KANTAN_CONFIG_DIR)
        self.config_dir_path = os.path.join(kantan_home, config_name)

        super().__init__(*args, **kwargs)

    def post_setup(self, context: SimpleNamespace) -> None:
        """
        Set up any virtual environment being created based on target
        configuration in KANTAN_CONFIG_DIR.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        config_file_path = os.path.join(self.config_dir_path, self.KANTAN_CONFIG_FILE)
        if os.path.exists(self.config_dir_path):
            if os.path.isfile(config_file_path):
                with open(config_file_path, "r", encoding="utf8") as config_file:
                    config = json.load(config_file)

                    if "requirements" in config:
                        for package_ref in config["requirements"]:
                            KantanEnvBuilder._install_dependency(context, package_ref)

                    if "include_files" in config:
                        for file_path in config["include_files"]:
                            KantanEnvBuilder._copy_file_to_env_dir(
                                context, self.config_dir_path, file_path
                            )
        else:
            logger.error("No configuration file %s does not exist", config_file_path)

    @staticmethod
    def _install_dependency(context: SimpleNamespace, package_ref: str) -> None:
        logger.debug("Installing %s package in %s", package_ref, context.bin_path)

        cmd = [context.env_exe, "-m", "pip", "install"]
        cmd.append(package_ref)
        subprocess.check_call(cmd)

    @staticmethod
    def _copy_file_to_env_dir(
        context: SimpleNamespace, config_dir_path: str, file_path: str
    ) -> None:
        if not os.path.isabs(file_path):
            file_path = os.path.join(config_dir_path, file_path)
        file_dir, file_name = os.path.split(file_path)
        dst_path = os.path.join(context.env_dir, file_name)

        logger.debug("Copying %s from %s to %s", file_name, file_dir, context.env_dir)
        shutil.copyfile(file_path, dst_path)
