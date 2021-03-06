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
import yaml
import re
from random import randint
import robot as r


class Tournament:

    @staticmethod
    def toId(thing):
        return re.sub(r'[^a-zA-z0-9,]', '', thing).lower()

    @staticmethod
    def buildRankingsTable(data, metagame):
        htmlString = '<h1 style="font-size:1em;">{}</h1>'.format(metagame)
        htmlString += '<table style="border-collapse: collapse; margin: 0; border: 1px solid black; width: 100%;}">'
        htmlString += '<tr><th style="border: 1px solid black;">Rank</th>'
        htmlString += '<th style="border: 1px solid black;">Name</th>'
        htmlString += '<th style="border: 1px solid black;">Tours</th>'
        htmlString += '<th style="border: 1px solid black;">Wins</th>'
        htmlString += '<th style="border: 1px solid black;">Win%</th></tr>'
        top10 = sorted(data.items(), key=lambda x: (x[1]['won'], x[1]['won'] / x[1]['entered']), reverse=True)[:10]
        rank = 1
        for person in top10:
            wins = person[1]['won']
            if wins < 1:
                continue
            entered = person[1]['entered']
            htmlString += '<tr style="{style} text-align: center;">'.format(style='background-color: #333333; color: #AAAAAA;' if rank % 2 == 0 else 'background-color: #AAAAAA; color: #333333;')
            htmlString += '<td>{rank}</td>'.format(rank=rank)
            htmlString += '<td>{player}</td>'.format(player=person[0])
            htmlString += '<td>{played}</td>'.format(played=entered)
            htmlString += '<td>{won}</td>'.format(won=wins)
            htmlString += '<td>{percent:.1f}</td></tr>'.format(percent=(wins / entered) * 100)
            rank += 1
        htmlString += '</table>'
        return htmlString

    def __init__(self, ws, room, tourFormat, battleHandler):
        self.ws = ws
        self.room = room
        self.format = tourFormat
        self.players = []
        self.hasStarted = False
        self.loggedParticipation = False
        self.bh = battleHandler

    def sendTourCmd(self, cmd):
        self.ws.send('{room}|/tour {cmd}'.format(room=self.room.title, cmd=cmd))

    def joinTour(self):
        self.sendTourCmd('join')

    def leaveTour(self):
        self.sendTourCmd('leave')

    def sendChallenge(self, opponent):
        self.sendTourCmd('challenge {opp}'.format(opp=opponent))

    def acceptChallenge(self):
        self.sendTourCmd('acceptchallenge')

    def pickTeam(self):
        team = self.bh.getRandomTeam(self.format)
        if team:
            self.ws.send('|/utm {}'.format(team))

    def onUpdate(self, msg):
        if 'updateEnd' in msg:
            return
        elif 'join'in msg:
            self.players.append(Tournament.toId(msg[1]))
        elif 'leave' in msg:
            self.players.remove(Tournament.toId(msg[1]))
        elif 'start' in msg:
            self.logParticipation()
        elif 'update' in msg:
            info = json.loads(msg[1])
            if 'challenges' in info and info['challenges']:
                self.pickTeam()
                self.sendChallenge(info['challenges'][0])
            elif 'challenged' in info and info['challenged']:
                self.pickTeam()
                self.acceptChallenge()
            elif 'isStarted' in info:
                self.hasStarted = info['isStarted']

    def logParticipation(self):
        with open('plugins/tournament-rankings.yaml', 'a+') as yf:
            yf.seek(0, 0)
            data = yaml.load(yf)
            if not data:
                data = {}
            if self.room.title not in data:
                data[self.room.title] = {}
            if self.format not in data[self.room.title]:
                data[self.room.title][self.format] = {}
            roomFormatData = data[self.room.title][self.format]
            for player in self.players:
                player = Tournament.toId(player)
                if player not in roomFormatData:
                    roomFormatData[player] = {'entered': 1, 'won': 0}
                else:
                    roomFormatData[player]['entered'] = roomFormatData[player]['entered'] + 1
            data[self.room.title][self.format] = roomFormatData
        with open('plugins/tournament-rankings.yaml', 'w') as yf:
            yaml.dump(data, yf, default_flow_style=False, explicit_start=True)
        self.loggedParticipation = True

    def logWin(self, winner):
        if not self.loggedParticipation:
            return  # This may happen if the bot joins midway through a tournament
        with open('plugins/tournament-rankings.yaml', 'a+') as yf:
            yf.seek(0, 0)
            data = yaml.load(yf)
            for user in winner:
                userData = data[self.room.title][self.format][Tournament.toId(user)]
                userData['won'] = userData['won'] + 1
        with open('plugins/tournament-rankings.yaml', 'w') as yf:
            yaml.dump(data, yf, default_flow_style=False, explicit_start=True)


def oldgentour(bot, cmd, room, msg, user):
    reply = r.ReplyObject('', True, True)
    if not room.tour:
        return reply.response('No tour is currently active, so this command '
                              'is disabled.')
    if not room.tour.format.startswith('gen'):
        return reply.response("The current tour isn't a previous generation, "
                              "so this command is disabled.")
    pastGens = {'gen1': 'RBY', 'gen2': 'GSC', 'gen3': 'RSE', 'gen4': 'DPP'}
    warning = ''
    if room.tour.format[0:4] in pastGens:
        warning = "/wall Please note that bringing Pokemon that aren't **{gen} NU** will disqualify you\n".format(gen=pastGens[room.tour.format[0:4]])
    return reply.response(warning + "/wall Sample teams here: http://www.smogon.com/forums/threads/3562659/")


def getranking(bot, cmd, room, msg, user):
    reply = r.ReplyObject('', True, True)
    if not user.hasRank('%') and not room.isPM:
        reply.response('Listing the rankings require Room Driver (%) or higher.')
    # format is room (optional), format, user (if ever, also optional)
    with open('plugins/tournament-rankings.yaml', 'r+') as yf:
        yf.seek(0, 0)
        data = yaml.load(yf)

    parts = list(map(bot.toId, msg.split(',')))
    roomTitle = ''
    try:
        roomData = data[parts[0]]
        roomTitle = parts.pop(0)
    except KeyError:
        roomData = data[room.title] if room.title in data else None
    try:
        formatData = roomData[parts[0]]
        format = parts.pop(0)
        try:
            userData = formatData[parts[0]]
            return reply.response('{user} has played {games} and won {wins} ({winrate:.1f}% win rate)'.format(use=parts[0], games=userData['entered'], wins=userData['won'], winrate=(userData['won'] / userData['entered']) * 100))
        except IndexError:
            rankingsTable = Tournament.buildRankingsTable(formatData, format)
            if bot.canHtml(room):
                return reply.response('/addhtmlbox {}'.format(rankingsTable))
            else:
                return reply.response('Cannot show full rankings in this room')
        except KeyError:
            return reply.response('{user} has no data for {tier} in {room}'.format(user=parts[0], tier=format, room=roomTitle if roomTitle else room.title))
    except TypeError:
        return reply.response('The room {} has no data about rankings'.format(msg.split(',')[0]))
    except IndexError:
        return reply.response('No format given')
    except KeyError:
        return reply.response('The room has no data about the format {}'.format(parts[0]))
