#!/usr/bin/env python3.6
"""Run script.
"""
import os
import shlex
import sys
from typing import List

from clinner.command import Type as CommandType
from clinner.command import command
from clinner.run.main import Main as ClinnerMain

APP_NAME = "goobox-nodes-scraper"
IMAGE_NAME = f"goobox/{APP_NAME}"
APP_PATH = f"/srv/apps/{APP_NAME}/app"


@command(command_type=CommandType.SHELL, parser_opts={"help": "Build docker image"})
def build(*args, **kwargs) -> List[List[str]]:
    tag = ["-t", f'{kwargs["image"]}:{kwargs["tag"]}']
    return [shlex.split(f"docker build") + tag + ["."] + list(args)]


@command(command_type=CommandType.SHELL, parser_opts={"help": "Push docker image"})
def push(*args, **kwargs) -> List[List[str]]:
    tag = [f'{kwargs["image"]}:{kwargs["tag"]}']
    return [shlex.split(f"docker push") + tag + list(args)]


@command(
    command_type=CommandType.SHELL,
    args=((("-p", "--port"), {"help": "App port", "default": "8000"}),),
    parser_opts={"help": "Run command through entrypoint"},
)
def run(*args, **kwargs) -> List[List[str]]:
    image = [f'{kwargs["image"]}:{kwargs["tag"]}']

    volumes = []
    if kwargs.get("source", None):
        volumes += ["-v", f"{os.getcwd()}:{APP_PATH}"]

    port = []
    if kwargs.get("port", None):
        port = ["-p", f'{kwargs["port"]}:8000']

    return [shlex.split(f"docker run") + port + volumes + image + list(args)]


@command(command_type=CommandType.SHELL, parser_opts={"help": "Run tests"})
def test(*args, **kwargs) -> List[List[str]]:
    kwargs["source"] = True
    return run("pytest", *args, **kwargs)


@command(command_type=CommandType.SHELL, parser_opts={"help": "Run lint"})
def lint(*args, **kwargs) -> List[List[str]]:
    kwargs["source"] = True
    return (
        run(*shlex.split("black --check ."), **kwargs)
        + run(*shlex.split("flake8"), **kwargs)
        + run(*shlex.split("isort --check-only"), **kwargs)
    )


class Main(ClinnerMain):
    def add_arguments(self, parser: "argparse.ArgumentParser"):
        super().add_arguments(parser)
        parser.add_argument("-i", "--image", help="Docker image name", default=IMAGE_NAME)
        parser.add_argument("-t", "--tag", help="Docker tag", default="latest")
        parser.add_argument("--source", help="Bind source code as docker volume", action="store_true")


if __name__ == "__main__":
    sys.exit(Main().run())
