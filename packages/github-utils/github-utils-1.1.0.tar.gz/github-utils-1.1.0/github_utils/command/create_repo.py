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
    parser.add_argument('--description', help='short description', metavar='DESC', default=NotSet)
    parser.add_argument('--homepage', help='url with more information', metavar='URL', default=NotSet)
    parser.add_argument('--private', action='store_true', help='private repository or not', default=False)
    parser.add_argument('--no-issues', action='store_true', help='disable issues', default=False)
    parser.add_argument('--no-wiki', action='store_true', help='disable wiki', default=False)
    parser.add_argument('--no-downloads', action='store_true', help='disable downloads', default=False)
    parser.add_argument('--team-id', help='team id to grant access', type=int, metavar='ID', default=NotSet)
    parser.add_argument('--auto-init', action='store_true', help='create initial commit', default=False)
    parser.add_argument('--gitignore', help='apply .gitignore template', metavar='LANG', default=NotSet)
    parser.add_argument('name', nargs='+', help='name of repository', default=NotSet)


def execute(config: GithubConfig, args: Namespace):
    gh = init_github(config)

    kwargs = {
        'description': args.description,
        'homepage': args.homepage,
        'private': args.private,
        'has_issues': (not args.no_issues),
        'has_wiki': (not args.no_wiki),
        'has_downloads': (not args.no_downloads),
        'auto_init': args.auto_init,
        'gitignore_template': args.gitignore
    }

    if args.organization is None:
        target = gh.get_user()
    else:
        target = gh.get_organization(args.organization)
        if args.team_id is not NotSet:
            team = target.get_team(args.team_id)
        else:
            team = NotSet

        kwargs['team_id'] = team

    for name in args.name:
        target.create_repo(name, **kwargs)

    return 0
