#!/usr/bin/env python3.6
"""Run script.
"""
import shlex
import sys
from typing import List

import os
from clinner.command import Type as CommandType, command
from clinner.run.main import Main

APP_NAME = 'goobox-nodes-scraper'
IMAGE_NAME = f'goobox/{APP_NAME}'
APP_PATH = f'/srv/apps/{APP_NAME}/app'
OUTPUT_PATH = f'/srv/apps/{APP_NAME}/output'


@command(command_type=CommandType.SHELL,
         args=((('-i', '--image'), {'help': 'Docker image name', 'default': IMAGE_NAME}),
               (('-t', '--tag'), {'help': 'Docker tag', 'default': 'latest'}),),
         parser_opts={'help': 'Build container'})
def build(*args, **kwargs) -> List[List[str]]:
    cmd = shlex.split(f'docker build -t {kwargs["image"]}/{kwargs["tag"]} .') + list(args)
    return [cmd]


@command(command_type=CommandType.SHELL,
         args=((('-i', '--image'), {'help': 'Docker image name', 'default': IMAGE_NAME}),
               (('-t', '--tag'), {'help': 'Docker tag', 'default': 'latest'}),
               (('--source',), {'help': 'Bind source code as docker volume', 'action': 'store_true'})),
         parser_opts={'help': 'Run command through entrypoint'})
def run(*args, **kwargs) -> List[List[str]]:
    image = [f'{kwargs["image"]}/{kwargs["tag"]}']

    os.makedirs('output', exist_ok=True)
    volumes = ['-v', f'{os.path.realpath("output")}:{OUTPUT_PATH}']
    if kwargs['source']:
        volumes += ['-v', f'{os.getcwd()}:{APP_PATH}']

    return [shlex.split(f'docker run') + volumes + image + list(args)]


@command(command_type=CommandType.SHELL,
         args=((('-i', '--image'), {'help': 'Docker image name', 'default': IMAGE_NAME}),
               (('-t', '--tag'), {'help': 'Docker tag', 'default': 'latest'}),
               (('--source',), {'help': 'Bind source code as docker volume', 'action': 'store_true'})),
         parser_opts={'help': 'Run tests'})
def test(*args, **kwargs) -> List[List[str]]:
    image = [f'{kwargs["image"]}/{kwargs["tag"]}']
    cmd = ['pytest']
    volumes = ['-v', f'{os.getcwd()}:{APP_PATH}'] if kwargs['source'] else []

    return [shlex.split(f'docker run') + volumes + image + cmd + list(args)]


if __name__ == '__main__':
    sys.exit(Main().run())
