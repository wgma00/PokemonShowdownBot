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

class Markov(object):
    '''This class will be used for determining what's the most probable message
       a user would say in a specific room
    '''
    def __init__(self, room_name):
        '''(Markov, str, str) -> None
            Initliazes the markov chain 
        '''
        self.room_name = room_name
        self.cache = {}

    
    def getTrips(self, words):
        '''(Markov, [str]) -> [(str,str,str)]
            Returns a list of triplets from the word database
        '''
        if len(words) < 3:
            return
        else:
            for i in range(len(words)-2):
                yield (words[i], words[i+1], words[i+2])

    def updateDatabase(self, message):
        '''(Markov, str) -> None
            Updates the database with this message
        '''
        # Parse the message and add it into the database
        for w1, w2, w3 in self.getTrips(message.split(' ')):
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generateMarkovText(self, size=25):
        '''(Markov, int) -> str'''
        seed = randomint(0, self.word_size-3)
        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            w1, w2, = w2, rand.choice(self.cache[(w1, w2)])
            gen_words.append(w2)
        return ' '.join(gen_words)


if __name__ == '__main__':
    m = Markov("test")

