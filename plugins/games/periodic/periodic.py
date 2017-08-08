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

import robot as r
import queue
import requests
import yaml
import random
import datetime

if __name__ == '__main__':
    from games import GenericGame
else:
    from plugins.games.game import GenericGame

ELEM = {'h', 'd', 't', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar',
        'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb',
        'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba',
        'la', 'ce', 'pr', 'nd', 'pm', 'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'lu', 'hf', 'ta', 'w',
        're', 'os', 'ir', 'pt', 'au', 'hg', 'tl', 'pb', 'bi', 'po', 'at', 'rn', 'fr', 'ra', 'ac', 'th', 'pa', 'u',
        'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr', 'rf', 'db', 'sg', 'bh', 'hs', 'mt', 'ds',
        'rg', 'cn', 'uut', 'uuq', 'uup', 'uuh', 'nh', 'og'}

WORDS = []
Scoreboard = {}
with open('plugins/games/periodic/periodic_scoreboard.yaml', 'a+') as yf:
    yf.seek(0, 0)
    Scoreboard = yaml.load(yf)
    # Empty yaml file set Scoreboard to None, but a dict is expected
    if not Scoreboard:
        Scoreboard = {}


class Periodic(GenericGame):
    """

    """

    def __init__(self):
        global WORDS
        if __name__ != '__main__':
            with open("plugins/games/periodic/word_dict.yaml", 'r') as yaml_file:
                self.details = yaml.load(yaml_file)
                if 'WORDS' in self.details and len(self.details['WORDS']) != 0:
                    WORDS = self.details['WORDS']
                else:
                    self.generate()
        else:
            with open("word_dict.yaml", 'r') as yaml_file:
                self.details = yaml.load(yaml_file)
                if 'WORDS' in self.details and len(self.details['WORDS']) != 0:
                    WORDS = self.details['WORDS']
                else:
                    self.generate()
        self.hints = []
        self.word = ''
        self.solution = ''
        self.startTime = 0
        self.new_game()

    def upload_words(self):
        global WORDS
        word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        response = requests.get(word_site)
        WORDS = [i.decode('utf-8') for i in response.content.splitlines()]
        self.details['WORDS'] = WORDS

    def generate(self):
        global WORDS
        self.details['WORDS'] = []
        self.upload_words()
        temp_words = []
        for word in WORDS:
            word = word.lower()
            ans = self.parse_text(word)
            if not ans:
                temp_words.append(word)
        WORDS = temp_words
        self.details['WORDS'] = WORDS

        if __name__ == '__main__':
            with open('word_dict.yaml', 'w') as outfile:
                outfile.write(yaml.dump(self.details, default_flow_style=False))
        else:
            with open('plugins/word_dict.yaml', 'w') as outfile:
                outfile.write(yaml.dump(self.details, default_flow_style=False))

    def new_game(self, user_input=''):
        global WORDS
        word = user_input if user_input else random.choice(WORDS)
        solution = self.parse_text(word)
        # invalid user input
        if not solution:
            word = random.choice(WORDS)
            solution = self.parse_text(word)
        self.hints = [("The correct answer has {elem} element(s)"
                       "").format(elem=len(solution)),
                      "The first element used is: " + solution[0],
                      "The last element used is: " + solution[-1]]
        self.startTime = datetime.datetime.now()
        self.word, self.solution = word, solution

    def _parse_text_bfs(self, txt):
        visited, q = set(), queue.Queue()
        q.put((txt, []))
        while not q.empty():
            val = q.get()
            if val[0] == '':
                return val[1]
            for key in ELEM:
                if val[0].startswith(key) and val[0][len(key):] not in visited:
                    visited.add(val[0][len(key):])
                    q.put((val[0][len(key):], val[1] + [key]))
        return None

    def parse_text(self, txt):
        txt = txt.replace(' ', '')
        txt = txt.lower()
        return self._parse_text_bfs(txt)

    def get_word(self):
        return self.word

    def get_solution(self):
        return self.solution

    def get_hint(self):
        if self.hints:
            hint = random.choice(self.hints)
            self.hints.remove(hint)
            return hint
        else:
            return "no more hints"

    def check_ans(self, ans):
        global ELEM
        print('checking: ', len(self.solution), self.solution, len(ans), ans)
        # we don't have to bother with these
        if len(ans) < len(self.solution) or len(ans) > len(self.solution):
            return False
        # check if it's the same predetermined solution
        first_test = True
        for i in range(len(self.solution)):
            if self.solution[i] != ans[i]:
                first_test = False
        # check if it's a valid solution of the same length
        tmp = self.word
        second_test = True
        for i in range(len(ans)):
            if tmp.startswith(ans[i]) and ans[i] in ELEM:
                tmp = tmp[len(ans[i]):]
            else:
                second_test = False
        return first_test or second_test

    def make_game(self, txt):
        self.word = txt
        self.solution = self.parse_text(self.word)

    def getSolveTimeStr(self):
        totalTime = datetime.datetime.now() - self.startTime
        if totalTime.seconds < 60:
            return ' in {time} seconds!'.format(time=totalTime.seconds)
        # Under 1 hour
        elif totalTime.seconds < 60 * 60:
            minutes = totalTime.seconds // 60
            return ' in {mins} minutes and {sec} seconds!'.format(mins=minutes, sec=totalTime.seconds - (minutes * 60))
        else:
            return '!'


def _parse_text_bfs(txt):
    visited, q = set(), queue.Queue()
    q.put((txt, []))
    while not q.empty():
        val = q.get()
        if val[0] == '':
            return val[1]
        for key in ELEM:
            if val[0].startswith(key) and val[0][len(key):] not in visited:
                visited.add(val[0][len(key):])
                q.put((val[0][len(key):], val[1] + [key]))
    return None


def parse_text(txt):
    words = []
    for i in txt:
        if i.isalpha():
            words.append(i)
    txt = ''.join(words)
    txt = txt.lower()
    return _parse_text_bfs(txt)

WHITELIST = ['cryolite', 'crimsonchin', 'octbot']
WHITELIST_RANK = '%'
PERIODIC_OBJ = Periodic()


def start(bot, cmd, room, msg, user):
    global WHITELIST
    reply = r.ReplyObject('', True, False, True, True, True)
    if msg.startswith("'") and msg.endswith("'") or (msg.startswith('"') and msg.endswith('"')):
        return str(parse_text(msg))
    if room.title == 'pm' and not cmd.startswith('score'):
        return reply.response("Don't try to play games in pm please")
    if msg == 'new':
        if not user.hasRank(WHITELIST_RANK) and user.id not in WHITELIST:
            return reply.response('You do not have permission to start a game in this room. (Requires {rank})'.format(rank=WHITELIST_RANK))
        if room.activity:
            return reply.response('A game is already running somewhere')
        if not room.allowGames:
            return reply.response('This room does not support chat games.')
        room.activity = PERIODIC_OBJ
        room.activity.new_game()
        return reply.response('A new periodic game has been created (guess with .pa):\n' + room.activity.get_word())

    elif msg == 'hint':
        if room.activity:
            return reply.response('The hint is: ' + room.activity.get_hint())
        return reply.response('There is no active periodic game right now')

    elif msg == 'help':
        if room.activity:
            return reply.response('Here\'s a periodic table: ' + 'http://imgur.com/t/periodic_table/iolEzW4')
        return reply.response('There is no active periodic game right now')

    elif msg == 'end':
        if not user.hasRank(WHITELIST_RANK) and user.id not in WHITELIST:
            return reply.response(('You do not have permission to end the periodic game. (Requires {rank})'
                                   '').format(rank=WHITELIST_RANK))
        if not (room.activity and room.activity.isThisGame(Periodic)):
            return reply.response('There is no active periodic game or a different game is active.')
        solved = room.activity.get_solution()
        room.activity = None
        return reply.response(('The periodic game was forcefully ended by {baduser}. (Killjoy)\nThe solution was: '
                               '**{solved}**').format(baduser=user.name, solved=solved))

    elif msg.lower().startswith('score'):
        if msg.strip() == 'score':
            msg += ' {user}'.format(user=user.id)
        name = bot.toId(msg[len('score '):])
        if name not in Scoreboard:
            return reply.response("This user never won any periodic games")
        return reply.response('This user has won {number} periodic game(s)'.format(number=Scoreboard[name]))
    else:
        if msg:
            return reply.response(('{param} is not a valid parameter for periodic. Make guesses with .pa'
                                   '').format(param=msg))
        if room.activity and room.activity.isThisGame(Periodic):
            return reply.response('Current periodic word: {word}'.format(word=room.activity.getWord()))
        return reply.response('There is no active periodic game right now')


def answer(bot, cmd, room, msg, user):
    reply = r.ReplyObject('', True, False, True, True, False)
    ans = list(msg.lower().split(' '))
    if not (room.activity and room.activity.isThisGame(Periodic)):
        return reply.response('There is no periodic game active right now')
    if room.activity.check_ans(ans):
        solved = room.activity.get_solution()
        timeTaken = room.activity.getSolveTimeStr()
        room.activity = None
        # lambda expression to determine the user's score

        def start_score(u, s):
            return 1 if(u not in s) else s[u] + 1

        Scoreboard[user.id] = start_score(user.id, Scoreboard)
        with open('plugins/periodic_scoreboard.yaml', 'w') as ym:
            yaml.dump(Scoreboard, ym)
        return reply.response(('Congratulations, {name} got it{time}\n'
                               'The solution was: {solution}').format(name=user.name, time=timeTaken, solution=solved))
    return reply.response('{test} is wrong!'.format(test=msg.lstrip()))


if __name__ == '__main__':
    PERIODIC_OBJ.make_game('puccini')
    print(PERIODIC_OBJ.check_ans('pu c c i ni'.split(' ')))
    print(PERIODIC_OBJ.check_ans('pu c c i ni'.split(' ')))
