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

# credit to Shadba Raaj for sample code that this was adapted from
# http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/

import random
import os


class Markov(object):
    """ This will generate messages based on the messages in a room.
   
    Specifically it will use Markov Chains to generate the messages. In this 
    case we will do it by every second word.

    Atrributes:
        room_name: string, name of the room we are in.
        file_name: string, path to the file we are going to store the room's 
                   messages in.
        cache: map a pair of strings to a words occurences, this will be 
               the rule we use to generate sentences.
        cache_len: maps a tuple to amount of words that come after this tuple.
        msg_cache: list of str, this will hold all the messages that have been
                   recorded thus far.
    """
    def __init__(self, room_name, file_name = None):
        """Intializes the database and starts creating the rules for grammar"""
        self.room_name = room_name
        self.file_name = ''
        if file_name is None:
            self.file_name = "roomdata-"+room_name+".txt"  
        else:
            self.file_name = file_name
        self.cache = {}
        self.cache_len = {}
        self.msg_cache = list(self.getFromFile())
        for msg in self.msg_cache:
            orig_msg = ''
            for word in msg:
                orig_msg += word + ' '
            self.updateDatabase(orig_msg.strip())


    def getFromFile(self):
        """Gets information from the database.
        Yields:
            list of str, a list of the sentences that were mentioned in chat.
        Raises:
            FileException: no file found.
        """
        with open(self.file_name, 'a+') as open_file: 
            open_file.seek(0, 0)
            for line in open_file:
                # we're removing periods to avoid a possible infinite 
                # loop in our rules
                line = line.strip().split(' ')
                yield line        

    def putToFile(self, msg):
        """Writes information from the database to file."""
        open_file = open(self.file_name, 'a') 
        open_file.write(msg + '\n' if '\n' not in msg else '')
        open_file.close()

    def getQuads(self, new_words):
        """Returns a list of quadrupalets generated from the sentence.
        Args:
            new_words: string, sentence that tuples will be generated from.
        Yields:
            list of string quadrupalets. 
        """
        if len(new_words) < 4:
            return
        else:
            # we will map the beginning of an arbitrary sentence ('.', '.') to
            # the start of an actual sentence 
            yield (' ', ' ', ' ', new_words[0]) 
            yield (' ', ' ', new_words[0], new_words[1])
            yield (' ', new_words[0], new_words[1], new_words[2])
            for i in range(len(new_words)-3):
                yield (new_words[i], new_words[i+1], new_words[i+2], new_words[i+3])
            # we will map the end of a word to a end of sentence, then the end
            # of a sentence to the start of an arbitrary sentence
            yield (new_words[-3], new_words[-2], new_words[-1], ' ')
            yield (new_words[-2], new_words[-1], ' ', ' ')
            yield (new_words[-1], ' ', ' ', ' ')

    def updateDatabase(self, msg, new_msg=False):
        """ Adds a word to the database and writes it to file.

        This is the method where we update the database and set the rule for
        the markov chain later on. Here the rule is that every two words will
        map to another. For example: ('Hello', 'darkness') -> 'my'. Also note 
        that since the database disjoint we attempt to unite them by adding a
        period after every sentence. For example: 'Hello darkness my old 
        friend' would be split to ('.', '.') -> 'Hello, ('.','Hello') ->
        'darkness', ..., ('friend', '.') -> '.'. Where '.' is a whitespace
        character. This is done since PS doesn't allow more than one whitespace
        to occur at the start of a sentence.

        Args:
            msg: string, sentence that will be added to the database.
            new_msg: Bool, if this message should be written to file.
        Returns:
            None.
        """
        # record the entries in our database 
        # if it isn't already
        if new_msg:
            self.putToFile(msg)
        # Parse the message and add it into the database
        for w1, w2, w3, w4 in self.getQuads(msg.strip().split(' ')):
            key = (w1, w2, w3)
            if key in self.cache and w4 in self.cache[key]:
                self.cache[key][w4] += 1
                self.cache_len[key] += 1
            elif key in self.cache and w4 not in self.cache[key]: 
                self.cache[key][w4] = 1
                self.cache_len[key] += 1
            else:
                self.cache[key] = {}
                self.cache[key][w4] = 1
                self.cache_len[key] = 1


    def chooseWord(self, key):
        """Chooses a word based from the cache list.

        Chooses a word uniformly by taking into account the probability of each
        word occuring.
        
        Args:
            key: string tuple, the key word we want to chose a word from.
        """
        seed = random.randint(0, self.cache_len[key]-1)
        tot = 0
        for i in self.cache[key]:
            tot += self.cache[key][i]
            if tot >= seed:
                return i
        # just return a random element in case I messed up
        return next (iter (self.cache[key].values()))



    def generateText(self, size=20):
        """Generates a sentence using the rules set we have defined 

        Args:
            size: int, the amount of words that we would like to generate
        Return:
            string, generated using Markov chains and the rules defined.
        Raise:
            None.
        """
        # we will start the seed at with words listed under the arbitrary
        # sentence
        seed_word, mid_word, next_word = ' ', ' ', self.chooseWord((' ',' ',' '))
        w1, w2, w3 = seed_word, mid_word, next_word
        gen_words = []
        # we'll skip printing the beginning
        sen_cnt = 2 
        while sen_cnt >= 0: 
            if w1 != ' ':
                gen_words.append(w1)
            w1, w2, w3 = w2, w3, self.chooseWord((w1, w2, w3)) 
            if (w1, w2, w3) == (' ',' ',' '):
                sen_cnt -= 1
        return ' '.join(gen_words)


if __name__ == '__main__':
    m = Markov("joim")
    print(m.generateText())
