# -*- coding: utf-8 -*-
# Copyright (C) 2020 HE Yaowen <he.yaowen@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import argparse
import importlib
from github_utils.helper import load_config


def print_help():
    usage = '''usage: gutils <command> [parameters]

    To see help text, you can run:
      gutils <command> --help
'''
    sys.stderr.write(usage)


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1][0] == '-':
        print_help()
        return -1

    parser = argparse.ArgumentParser()
    parser.add_argument('command')

    command = importlib.import_module('github_utils.command.%s' % (sys.argv[1].replace('-', '_')))
    command.add_arguments(parser)

    return command.execute(
        config=load_config('%s/.github-utils/config.ini' % (os.getenv('HOME'))),
        args=parser.parse_args()
    )


if __name__ == '__main__':
    sys.exit(main())
