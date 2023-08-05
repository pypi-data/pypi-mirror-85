import asyncio
import json
import os
import subprocess
import sys

import aiohttp
import dask
from distributed.compatibility import WINDOWS

from ..utils import parse_identifier

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def conda_command():
    return os.environ.get("CONDA_EXE", "conda")


def parse_conda_command(cmd: list):
    if not any("json" in i for i in cmd):
        raise ValueError(
            "Attempting to parse conda command output with no json options specified"
        )
    output = subprocess.check_output(cmd)
    result = json.loads(output)
    return result


def conda_package_versions(name: str) -> dict:
    """Return pacakge name and version for each conda installed pacakge

    Parameters
    ----------
    name
        Name of conda environment

    Returns
    -------
    results
        Mapping that contains the name and version of each installed package
        in the environment
    """
    cmd = [conda_command(), "env", "export", "-n", name, "--no-build", "--json"]
    output = parse_conda_command(cmd)
    output = output.get("dependencies", [])
    results = {}
    for i in output:
        if isinstance(i, str):
            package, version = i.split("=")
            results[package] = version
        else:
            # TODO: Use pip installed package information which is currently ignored
            assert isinstance(i, dict), type(i)
            assert list(i.keys()) == ["pip"], list(i.keys())
    return results


async def get_software_info(name: str) -> dict:
    """Retrieve solved spec for a Coiled software environment

    Parameters
    ----------
    name
        Software environment name

    Returns
    -------
    results
        Coiled software environment information
    """
    account, name = parse_identifier(name)
    account = account or dask.config.get("coiled.user")

    token = dask.config.get("coiled.token")
    async with aiohttp.ClientSession(
        headers={"Authorization": "Token " + token}
    ) as session:
        server = dask.config.get("coiled.server")
        response = await session.request(
            "GET",
            server + f"/api/v1/{account}/software_environments/{name}/",
        )
        if response.status >= 400:
            text = await response.text()
            if "Not found" in text:
                raise ValueError(
                    f"Could not find a {account}/{name} Coiled software environment"
                )
            else:
                raise Exception(text)

        results = await response.json()
        return results


def get_event_loop():
    """
    This works around an issue with torando and windows

    Dask has a possibly overly strict fix to this issue that we should consider
    toning down.  See distributed/utils.py and grep for this line:
    https://github.com/tornadoweb/tornado/issues/2608
    """
    if WINDOWS and sys.version_info >= (3, 8):
        return asyncio.ProactorEventLoop()  # type: ignore
    else:
        return asyncio.get_event_loop()
