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

import os
import configparser
import github
from dataclasses import dataclass


@dataclass
class GithubConfig:
    token: str


def load_config(filename) -> GithubConfig:
    if not os.path.exists(filename):
        raise Exception('configuration file "%s" not found.' % filename)

    config = configparser.ConfigParser()
    config.read(filename)

    return GithubConfig(
        token=config.get('auth', 'token')
    )


def init_github(config: GithubConfig):
    return github.Github(login_or_token=config.token)
