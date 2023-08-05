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

from argparse import ArgumentParser, Namespace
from github_utils.helper import GithubConfig, init_github
from github.GithubObject import NotSet


def add_arguments(parser: ArgumentParser):
    parser.add_argument('--organization', help='repository organization', metavar='ORG')
    parser.add_argument('--all', action='store_true', help='remove all repositories', default=False)
    parser.add_argument('name', nargs='*', help='name of repository', default=NotSet)


def execute(config: GithubConfig, args: Namespace):
    gh = init_github(config)

    if args.organization is None:
        target = gh.get_user()
    else:
        target = gh.get_organization(args.organization)

    if args.all:
        for repo in target.get_repos():
            repo.delete()
    else:
        for name in args.name:
            target.get_repo(name).delete()
