import json
import logging
import os
import shutil
import subprocess
import venv

logger = logging.getLogger(__name__)


def create(
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
        if os.path.exists(self.config_dir_path):
            config_file_path = os.path.join(self.config_dir_path, "configuration.json")
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

        logger.debug("Copying %s from %s to %s", file_name, file_dir, context.env_dir)
        shutil.copyfile(file_path, dst_path)
