#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
import shlex
from subprocess import PIPE, run
import sys
from typing import Dict, List, Optional, Set, Tuple
import warnings

class RefusalToBuildException(Exception):
    pass

ERROR_COLOR = '\033[01;31m'
NO_COLOR = '\033[00m'

# Would like to include timezone offset, but not worth the
# complexity of including pytz/etc.
TIMESTAMP_FORMAT = '%Y%m%d-%H%M%S%z'

# TODO: expand to other formats (JSON, YAML, CSV) in the future if necessary or appropriate
IMAGE_LIST_FILENAME = 'docker_images.txt'

BASE_DIR_BUILD_OPTION = 'base_directory_build'
GIT_VERSION_FILE_OPTION = 'write_git_version'

SUPPORTED_OPTIONS = frozenset({BASE_DIR_BUILD_OPTION, GIT_VERSION_FILE_OPTION})

DOCKER = 'docker'
DOCKER_BUILD_COMMAND_TEMPLATE: List[str] = [
    DOCKER,
    'build',
    '-q',
    '-t',
    '{label}',
    '-f',
    '{dockerfile_path}',
    '.',
]
DOCKER_TAG_COMMAND_TEMPLATE: List[str] = [
    DOCKER,
    'tag',
    '{image_id}',
    '{tag_name}',
]
DOCKER_PUSH_COMMAND_TEMPLATE: List[str] = [
    DOCKER,
    'push',
    '{image_id}',
]

GIT = 'git'
GIT_SUBMODULE_STATUS_COMMAND: List[str] = [
    GIT,
    'submodule',
    'status',
]
GIT_VERSION_COMMAND = [
    GIT,
    'describe',
    '--dirty',
    '--always',
    '--abbrev=12',
]

def print_run(command: List[str], pretend: bool, return_stdout: bool=False, **kwargs):
    if 'cwd' in kwargs:
        directory_piece = f' in directory "{kwargs["cwd"]}"'
    else:
        directory_piece = ''
    if pretend:
        print('Would run "{}"{}'.format(' '.join(command), directory_piece))
        return '<pretend>'
    else:
        print('Running "{}"{}'.format(' '.join(command), directory_piece))
        kwargs = kwargs.copy()
        if return_stdout:
            kwargs['stdout'] = PIPE
        proc = run(command, check=True, **kwargs)
        if return_stdout:
            return proc.stdout.strip().decode('utf-8')

def write_git_version(cwd: Path, dest_path: Path):
    try:
        proc = run(GIT_VERSION_COMMAND, cwd=cwd, stdout=PIPE, check=True)
        git_version = proc.stdout.decode('utf-8').strip()

        print('Writing Git version', git_version, 'to', dest_path)
        with open(dest_path, 'w') as f:
            print(git_version, file=f)
    except Exception as e:
        # don't care too much; this is best-effort
        print('Caught', e)

def read_images(directory: Path) -> List[Tuple[str, Path, Dict[str, Optional[str]]]]:
    """
    Reads an *ordered* list of Docker container/image information.
    Looks for 'docker_images.txt' in the given directory, and reads
    whitespace-separated lines. Piece 0 is the "base" name of the Docker
    container, without any tags, e.g. 'hubmap/codex-scripts', piece
    1 is the path to the matching Dockerfile, relative to this
    directory, and piece 2 is a string consisting of comma-separated
    options for the build.

    Lines starting with '#' are ignored.

    :param directory: directory containing `IMAGE_LIST_FILENAME`
    :return: List of (label, Dockerfile path, option set) tuples
    """
    images = []
    with open(directory / IMAGE_LIST_FILENAME) as f:
        for line in f:
            if line.startswith('#'):
                continue
            image, path, *rest = shlex.split(line)
            options = {}
            if rest:
                option_kv_list = rest[0].split(',')
                for kv_str in option_kv_list:
                    pieces = kv_str.split('=', 1)
                    value = pieces[1] if len(pieces) == 2 else None
                    options[pieces[0]] = value
            images.append((image, Path(path), options))
    return images

def check_submodules(directory: Path, ignore_missing_submodules: bool):
    submodule_status_output = run(
        GIT_SUBMODULE_STATUS_COMMAND,
        stdout=PIPE,
        cwd=directory,
    ).stdout.decode('utf-8').splitlines()

    # name, commit
    uninitialized_submodules: Set[Tuple[str, str]] = set()

    for line in submodule_status_output:
        status_code, pieces = line[0], line[1:].split()
        if status_code == '-':
            uninitialized_submodules.add((pieces[1], pieces[0]))

    if uninitialized_submodules:
        message_pieces = ['Found uninitialized submodules:']
        for name, commit in sorted(uninitialized_submodules):
            message_pieces.append(f'\t{name} (at commit {commit})')
        message_pieces.append("Maybe you need to run")
        message_pieces.append("\tgit submodule update --init")
        message_pieces.append("(Override with '--ignore-missing-submodules' if you're really sure.)")

        if not ignore_missing_submodules:
            raise RefusalToBuildException('\n'.join(message_pieces))

def check_options(options: Dict[str, Optional[str]]):
    unknown_options = set(options) - SUPPORTED_OPTIONS
    if unknown_options:
        option_str = ', '.join(sorted(unknown_options))
        # TODO: decide whether this is an error
        warnings.warn(f'Unsupported Docker option(s): {option_str}')

def tag_image(image_id: str, tag_name: str, pretend: bool):
    docker_tag_command = [
        piece.format(
            image_id=image_id,
            tag_name=tag_name,
        )
        for piece in DOCKER_TAG_COMMAND_TEMPLATE
    ]
    print_run(docker_tag_command, pretend)
    print('Tagged image', image_id, 'as', tag_name)

def build(tag_timestamp: bool, tag: Optional[str], push: bool, ignore_missing_submodules: bool, pretend: bool):
    base_directory = Path()
    docker_images = read_images(base_directory)
    check_submodules(base_directory, ignore_missing_submodules)
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    images_to_push = []
    for label_base, full_dockerfile_path, options in docker_images:
        label = f'{label_base}:latest'
        check_options(options)

        if GIT_VERSION_FILE_OPTION in options:
            git_version_file = Path(options[GIT_VERSION_FILE_OPTION])
            write_git_version(base_directory, git_version_file)

        # TODO: seriously reconsider this; it feels wrong
        if BASE_DIR_BUILD_OPTION in options:
            build_dir = Path()
        else:
            build_dir = full_dockerfile_path.parent

        dockerfile_path = full_dockerfile_path.relative_to(build_dir)
        docker_build_command = [
            piece.format(
                label=label,
                dockerfile_path=dockerfile_path,
            )
            for piece in DOCKER_BUILD_COMMAND_TEMPLATE
        ]
        image_id = print_run(docker_build_command, pretend, return_stdout=True, cwd=build_dir)
        images_to_push.append(label)
        print('Tagged image', image_id, 'as', label)

        if tag_timestamp:
            timestamp_tag_name = f'{label_base}:{timestamp}'
            tag_image(image_id, timestamp_tag_name, pretend)
            images_to_push.append(timestamp_tag_name)

        if tag is not None:
            tag_name = f'{label_base}:{tag}'
            tag_image(image_id, tag_name, pretend)
            images_to_push.append(tag_name)

    if push:
        for image_id in images_to_push:
            docker_push_command = [
                piece.format(
                    image_id=image_id,
                )
                for piece in DOCKER_PUSH_COMMAND_TEMPLATE
            ]
            print_run(docker_push_command, pretend)

def main():
    p = ArgumentParser()
    p.add_argument(
        '--tag-timestamp',
        action='store_true',
        help="""
            In addition to tagging images as "latest", also tag with a
            timestamp in "YYYYMMDD-HHmmss" format. All images in "docker_images.txt"
            are tagged with the same timestamp.
        """,
    )
    p.add_argument(
        '--tag',
        help="""
            In addition to tagging images as "latest", also tag with the tag name
            provided. All images in "docker_images.txt" are tagged with the same tag name.
        """,
    )
    p.add_argument(
        '--push',
        action='store_true',
        help="""
            Push all built containers to Docker Hub, tagged as "latest" and with any
            additional tags specified via "--tag-timestamp" or "--tag=tag_name".
        """,
    )
    p.add_argument(
        '--ignore-missing-submodules',
        action='store_true',
        help="""
            Allow building Docker containers if "git submodule" reports that at least
            one submodule is uninitialized.            
        """,
    )
    p.add_argument(
        '--pretend',
        action='store_true',
        help="""
            Run in pretend mode: don't actually execute anything (building, tagging, pushing).
        """,
    )
    args = p.parse_args()

    try:
        build(args.tag_timestamp, args.tag, args.push, args.ignore_missing_submodules, args.pretend)
    except RefusalToBuildException as e:
        print(ERROR_COLOR + 'Refusing to build Docker containers, for reason:' + NO_COLOR)
        sys.exit(e.args[0])

if __name__ == '__main__':
    main()
