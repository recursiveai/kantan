import os
import shutil
import sys
from pathlib import Path
from unittest.mock import PropertyMock, patch

from kantan.builder import create
from kantan.cli import run

_tests_root = Path(__file__).parent


def _assert_venv(env_dir: str):
    version_info = sys.version_info
    python_version = f"{version_info[0]}.{version_info[1]}"
    assert os.path.exists(os.path.abspath(env_dir))
    assert os.path.exists(os.path.join(os.path.abspath(env_dir), "pip.conf"))
    assert os.path.exists(
        os.path.join(
            os.path.abspath(env_dir),
            "lib",
            f"python{python_version}",
            "site-packages",
            "kantan",
        )
    )


def _cleanup(env_dir: str):
    shutil.rmtree(os.path.abspath(env_dir))


@patch(
    "kantan.builder.KantanEnvBuilder.KANTAN_CONFIG_DIR",
    new_callable=PropertyMock,
    return_value=f"{_tests_root}",
)
def test_venv_creation(_):
    env_dir = ".test_1"
    create(
        env_dir,
        system_site_packages=False,
        clear=False,
        symlinks=True,
        upgrade=False,
        with_pip=True,
        prompt=None,
        upgrade_deps=False,
        config_name="fixtures",
    )
    _assert_venv(env_dir)
    _cleanup(env_dir)


@patch(
    "kantan.builder.KantanEnvBuilder.KANTAN_CONFIG_DIR",
    new_callable=PropertyMock,
    return_value=f"{_tests_root}",
)
def test_venv_creation_cli(_):
    env_dir = ".test_2"
    run([env_dir, "--config-name", "fixtures"])
    _assert_venv(env_dir)
    _cleanup(env_dir)
