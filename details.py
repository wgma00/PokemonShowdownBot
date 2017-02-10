# Copyright (C) 2016 William Granados<wiliam.granados@wgma00.me>
#
# This file is part of PokemonShowdownBot.
#
# PokemonShowdownBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PokemonShowdownBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PokemonShowdownBot.  If not, see <http://www.gnu.org/licenses/>.

import yaml
import re
import os


def to_id(thing):
    """Assigns a unique ID to everyone"""
    return re.sub(r'[^a-zA-z0-9,]', '', thing).lower()

try:
    with open("details.yaml", 'r') as yaml_file:
        details = yaml.load(yaml_file)
        bot_name = details['user']
        master = to_id(details['master'])
        password = details['password']
        bot_id = to_id(bot_name)
        command_char = details['command']
        avatar = details['avatar']
        debug = details['debug']
        joinRooms = details['joinRooms']
        client_id = details['imgur_apikey']
        api_key = details['apikey']
except FileNotFoundError as e:
    print('details.yaml not found')
    try:
        bot_name = 'quadbot'
        master = 'wgma'
        password = ''
        bot_id = to_id(bot_name)
        command_char = '.'
        avatar = 0
        debug = False
        joinRooms = []
        client_id = os.environ['IMGUR_API']
        api_key = '0'
    except Exception:
        print('No environment variables for testing on Travis CI')
        print('Please follow instructions for running the bot in README.md')
