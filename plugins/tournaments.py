# The MIT License (MIT)
#
# Copyright (c) 2015 QuiteQuiet<https://github.com/QuiteQuiet>
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

import json
from random import randint
import robot as r

class Tournament:
    def __init__(self, ws, roomName, tourFormat):
        self.ws = ws
        self.room = roomName
        self.format = tourFormat
        self.hasStarted = False


    def sendTourCmd(self, cmd):
        self.ws.send('{room}|/tour {cmd}'.format(room=self.room, cmd=cmd))

    def joinTour(self):
        self.sendTourCmd('join')

    def leaveTour(self):
        self.sendTourCmd('leave')

    def sendChallenge(self, opponent):
        self.sendTourCmd('challenge {opp}'.format(opp = opponent))

    def acceptChallenge(self):
        self.sendTourCmd('acceptchallenge')

    def onUpdate(self, msg):
        if 'updateEnd' in msg : return
        if 'update' in msg:
            info = json.loads(msg[1])
            if 'challenges' in info and info['challenges']:
                self.sendChallenge(info['challenges'][0])
            elif 'challenged' in info and info['challenged']:
                self.acceptChallenge()
            elif 'isStarted' in info:
                self.hasStarted = info['isStarted']

def oldgentour(bot, cmd, room, msg, user):
    reply = r.ReplyObject('', True, True)
    if not room.tour:
        return reply.response('No tour is currently active, so this command '
                              'is disabled.')
    if not room.tour.format.startswith('gen'):
        return reply.response("The current tour isn't a previous generation, "
                              "so this command is disabled.")
    pastGens = {'gen1': 'RBY', 'gen2':'GSC', 'gen3':'RSE',  'gen4':'DPP'}
    warning = ''
    if room.tour.format[0:4] in pastGens:
        warning = ("/wall Please note that bringing Pokemon that aren't "
                  "**{gen} NU** will disqualify you\n"
                  "").format(gen=pastGens[room.tour.format[0:4]])
    return reply.response(warning+("/wall Sample teams here: "
                                   "http://www.smogon.com/forums/threads/"
                                   "3562659/"))

