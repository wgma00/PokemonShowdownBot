# The MIT License (MIT)
#
# Copyright (c) 2015
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# credit to Shadba Raaj for sample code
# http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/

import random

class Markov(object):
    '''This class will be used for determining what's the most probable message
       a user would say in a specific room
    '''
    def __init__(self, room_name, file_name = None):
        '''(Markov, str, str) -> None
            Initliazes the markov chain 
        '''
        self.room_name = room_name
        self.file_name = file_name if file_name != None else "roomdata-"+room_name+".txt"  
        self.cache = {}
        self.msg_cache = list(self.getFromFile())
        self.words = [] 
        for msg in self.msg_cache:
            orig_msg = ''
            for word in msg:
                orig_msg += word + ' '
                self.words.append(word)
            self.updateDatabase(orig_msg.strip())


    def getFromFile(self):
        '''(Markov) -> [str]
            Returns the messages that were recorded for this chatroom
        '''
        open_file = open(self.file_name, 'r') 
        for line in open_file:
            line = line.strip().split(' ')
            yield line        
        open_file.close()

    def putToFile(self, msg):
        '''(Markov, str) -> None
            Record information for future usage 
        '''
        open_file = open(self.file_name, 'a') 
        open_file.write(msg + '\n' if '\n' not in msg else '')
        open_file.close()

    def getTrips(self, new_words):
        '''(Markov, [str]) -> [(str,str,str)]
            Returns a list of triplets from the word database
        '''
        if len(new_words) < 3:
            return
        else:
            # we will map the beginning of an arbitrary sentence ('.', '.') to
            # the start of an actual sentence 
            yield ('.', '.', new_words[0])
            yield ('.', new_words[0], new_words[1])
            for i in range(len(new_words)-2):
                yield (new_words[i], new_words[i+1], new_words[i+2])
            # we will map the end of a word to a end of sentence, then the end
            # of a sentence to the start of an arbitrary sentence
            yield ( new_words[-2], new_words[-1], '.')
            yield ( new_words[-1], '.', '.')

    def updateDatabase(self, msg, new_msg=False):
        '''(Markov, str) -> None
            Updates the database with this message
        '''
        # record the entries in our database 
        # if it isn't already
        if new_msg:
            self.putToFile(msg)
            for word in msg.strip().split(' '):
                self.words.append(word)
        # Parse the message and add it into the database
        for w1, w2, w3 in self.getTrips(msg.strip().split(' ')):
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generateMarkovText(self, size=10):
        '''(Markov, int) -> str
            generate some random text based on the most likely set of words 
        '''
        # we will start the seed at with words listed under the arbitrary
        # sentence
        seed = random.randint(0, len(self.cache[('.','.')])-1)
        seed_word, next_word = '.', self.cache[('.','.')][seed] 
        w1, w2 = seed_word, next_word
        gen_words = []
        # we'll skip printing the beginning
        for i in range(size):
            if w1 != '.':
                gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)]) 
            if w2 != '.':
                gen_words.append(w2)
        return ' '.join(gen_words)


if __name__ == '__main__':
    m = Markov("scholastic")
    print(m.generateMarkovText())
    # print(m.generateMarkovText())

