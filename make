#!/usr/bin/env python3.6
"""Run script.
"""
import shlex
import sys
from typing import List

from clinner.command import Type as CommandType, command
from clinner.run.main import Main

APP_NAME = 'goobox-nodes-scraper'
IMAGE_NAME = f'goobox/{APP_NAME}'


@command(command_type=CommandType.SHELL,
         args=((('-i', '--image'), {'help': 'Docker image name', 'default': IMAGE_NAME}),
               (('-t', '--tag'), {'help': 'Docker tag', 'default': 'latest'}),),
         parser_opts={'help': 'Build container'})
def build(*args, **kwargs) -> List[List[str]]:
    cmd = shlex.split(f'docker build -t {kwargs["image"]}/{kwargs["tag"]} .') + list(args)
    return [cmd]


@command(command_type=CommandType.SHELL,
         args=((('-i', '--image'), {'help': 'Docker image name', 'default': IMAGE_NAME}),
               (('-t', '--tag'), {'help': 'Docker tag', 'default': 'latest'}),),
         parser_opts={'help': 'Run command through entrypoint'})
def run(*args, **kwargs) -> List[List[str]]:
    cmd = shlex.split(f'docker run {kwargs["image"]}/{kwargs["tag"]}') + list(args)
    return [cmd]


@command(command_type=CommandType.SHELL,
         args=((('-i', '--image'), {'help': 'Docker image name', 'default': IMAGE_NAME}),
               (('-t', '--tag'), {'help': 'Docker tag', 'default': 'latest'}),),
         parser_opts={'help': 'Run tests'})
def test(*args, **kwargs) -> List[List[str]]:
    cmd = shlex.split(f'docker run {kwargs["image"]}/{kwargs["tag"]} pytest') + list(args)
    return [cmd]


if __name__ == '__main__':
    sys.exit(Main().run())
