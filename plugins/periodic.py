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

import queue
import requests
import yaml
import random

if __name__ == '__main__':
    from games import GenericGame
else:
    from plugins.games import GenericGame

ELEM = {'h':1,'d':1, 't':1, 'he':2, 'li':3, 'be':4, 'b':5, 'c':6, 'n':7, 'o':8,
        'f':9, 'ne':10, 'na':11, 'mg':12, 'al':13, 'si':14, 'p':15, 's':16,
        'cl':17, 'ar':18, 'k':19, 'ca':20, 'sc':21, 'ti':22, 'v':23, 'cr':24,
        'mn':25, 'fe':26, 'co':27, 'ni':28, 'cu':29, 'zn':30, 'ga':31, 'ge':32,
        'as':33, 'se':34, 'br':35, 'kr':36, 'rb':37, 'sr':38, 'y':39, 'zr':40,
        'nb':41, 'mo':42, 'tc':43, 'ru':44, 'rh':45, 'pd':46, 'ag':47, 'cd':48,
        'in':49, 'sn':50, 'sb':51, 'te':52, 'i':53, 'xe':54, 'cs':55, 'ba':56, 
        'la':57, 'ce':58, 'pr':59, 'nd':60, 'pm':61, 'sm':62, 'eu':63, 'gd':64,
        'tb':65, 'dy':66, 'ho':67, 'er':68, 'tm':69, 'yb':70, 'lu':71, 'hf':72,
        'ta':73, 'w':74, 're':75, 'os':76, 'ir':77, 'pt':78, 'au':79, 'hg':80, 
        'tl':81, 'pb':82, 'bi':83, 'po':84, 'at':85, 'rn':86, 'fr':87, 'ra':88,
        'ac':89, 'th':90, 'pa':91, 'u':92, 'np':93, 'pu':94, 'am':95, 'cm':96,
        'bk':97, 'cf':98, 'es':99, 'fm':100, 'md':101, 'no':102, 'lr':103,
        'rf':104, 'db':105, 'sg':106, 'bh':107, 'hs':108, 'mt':109, 'ds':110,
        'rg':111, 'cn':112, 'uut':113, 'uuq':114, 'uup':115, 'uuh':116,
        'nh':117, 'og':118} 

WORDS = [] 

class Periodic(GenericGame):
    def __init__(self):
        global WORDS
        if __name__ != '__main__':
            with open("plugins/word_dict.yaml", 'r') as yaml_file:
                self.details = yaml.load(yaml_file)
                if('WORDS' in self.details and len(self.details['WORDS']) != 0): 
                    WORDS = self.details['WORDS']
                else:
                    self.generate()
        else:
            with open("word_dict.yaml", 'r') as yaml_file:
                self.details = yaml.load(yaml_file)
                if('WORDS' in self.details and len(self.details['WORDS']) != 0):
                    WORDS = self.details['WORDS']
                else:
                    self.generate()
        self.hints = []
        self.word = ''
        self.solution = ''
        self.new_game()


    def upload_words(self):
        global WORDS
        word_site = ("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&"
                     "content-type=text/plain")
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
            if ans != None:
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
        #invalid user input
        if(solution == None):
            word = random.choice(WORDS)
            solution = self.parse_text(word)
        self.hints = ["The correct answer has {elem} element(s)".format(elem=len(solution)),
                      "The first element used is: " + solution[0],
                      "The last element used is: " + solution[-1]]
        self.word, self.solution = word, solution

    def _parse_text_bfs(self, txt):
        visited, q = set(), queue.Queue()
        q.put((txt,[]))
        while not q.empty():
            val = q.get()
            if val[0] == '':
                return val[1]
            for key in ELEM:
                if val[0].startswith(key) and val[0][len(key):] not in visited:
                    visited.add(val[0][len(key):])
                    q.put((val[0][len(key):],val[1]+[key])) 
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
        print('checking: ',len(self.solution), self.solution, len(ans), ans)
        # we don't have to bother with these
        if(len(ans) < len(self.solution) or len(ans) > len(self.solution)):
            return False
        # check if it's the same pretdetermined solution
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

def _parse_text_bfs(txt):
    visited, q = set(), queue.Queue()
    q.put((txt,[]))
    while not q.empty():
        val = q.get()
        if val[0] == '':
            return val[1]
        for key in ELEM:
            if val[0].startswith(key) and val[0][len(key):] not in visited:
                visited.add(val[0][len(key):])
                q.put((val[0][len(key):],val[1]+[key])) 
    return None

def parse_text(txt):
    words = []
    for i in txt:
        if i.isalpha():
            words.append(i)
    txt = ''.join(words)
    txt = txt.lower()
    return _parse_text_bfs(txt)

WHITELIST = ['cryolite']
PERIODIC_OBJ = Periodic()

def start(bot, cmd, room, msg, user):
    
    if (msg.startswith("'") and msg.endswith("'")
        or (msg.startswith('"') and msg.endswith('"'))):
        return str(parse_text(msg)), True
        
    if msg == 'new': 
        global WHITELIST
        global PERIODIC_OBJ
        if not user.hasRank('+') and (not user.name.strip() in WHITELIST):
            return 'You do not have permission to start a game in this room. (Requires +)', False
        if room.game:                                                           
            return 'A game is already running somewhere', False                 
        room.game = PERIODIC_OBJ 
        room.game.new_game()
        return 'A new periodic parsed word has been created (guess with .pa):\n' + room.game.get_word(), True

    elif room.game and msg == 'hint':
        return room.game.get_hint(), True

    elif room.game and msg == 'end':
        if not user.hasRank('+'):                                               
            return 'You do not have permission to end the anagram. (Requires +)', True

        solved = room.game.get_solution()                                      
        room.game = None
        return ('The anagram was forcefully ended by {baduser}.'
                 ' (Killjoy)\nThe solution was: **{solved}**'
                 '').format(baduser=user.name,solved=solved), True

    else:                                                                                                                                         
           if msg: return '{param} is not a valid parameter for .periodic. Make guesses with .pa'.format(param = msg), False
           if room.game:                         
               return 'Current periodic word: {word}'.format(word = room.game.get_word()), True
           return 'There is no active anagram right now', False          

def answer(bot, cmd, room, msg, user):
    ans = list(msg.lower().split(' '))
    if room.game:
        if(room.game.check_ans(ans)):
            sln = room.game.get_solution()
            room.game = None
            return 'Congratulations! The solution was: {solution}'.format(name=user.name, solution=sln), True     
        else:
            return '{test} is wrong!'.format(test=msg.lstrip()), True 
    else:
        return 'There is no game running currently', True

if __name__ == '__main__':
    PERIODIC_OBJ.make_game('puccini')
    print(PERIODIC_OBJ.check_ans('pu c c i ni'.split(' ')))
    print(PERIODIC_OBJ.check_ans('pu c c i ni'.split(' ')))
    # print(parse_text('Nonrepresentationalisms')[1])


