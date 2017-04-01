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

class Pokemon:
    def __init__(self, ident, details, condition, active, stats, moves, baseAbility, item, canMegaEvo, slot):
        self.species = ident
        self.details = details
        self.condition = condition.split()[0]
        self.status = condition.split()[1] if ' ' in condition else ''
        self.active = active
        self.stats = stats
        self.moves = moves
        self.ability = baseAbility
        self.item = item
        self.canMega = canMegaEvo
        self.teamSlot = slot
        self.boosts = {'atk':0, 'def':0, 'spa':0, 'spd':0, 'spe':0, 'evasion':0, 'accuracy':0}
    def setCondition(self, cond, status):
        self.condition = cond
        self.status = status

class Player:
    def __init__(self):
        self.name = ''
        self.id = ''
        self.active = None
        self.team = {}
        self.side = {}
    def setActive(self, poke):
        self.active = poke
    def updateTeam(self, poke):
        self.team[poke.species] = poke
    def changeTeamSlot(self, old, new):
        if not old:
            for m in self.team:
                if self.team[m]:
                    old = self.team[m]
        old.teamSlot, new.teamSlot = new.teamSlot, old.teamSlot
    def getPokemon(self, species):
        for poke in self.team:
            if self.team[poke].species == species:
                return self.team[poke]
        # Logically this shouldn't happen, but apparently it does sometimes?
        raise AttributeError('{mon} isn\'t in the team'.format(mon = species))
    def removeBaseForm(self, pokemon, mega):
        self.team[mega] = self.team.pop(pokemon, None)
        self.team[mega].species = mega

class Battle:
    def __init__(self, name):
        self.rqid = 1
        self.myActiveData = {}
        self.me = Player()
        self.other = Player()
        self.field = {}
        self.spectating = False

    def setMe(self, me, pId):
        self.me.name = me
        self.me.id = pId
    def setOther(self, other, pId):
        self.other.name = other
        self.other.id = pId
    def setFieldCond(self, cond):
        # TODO: do this
        pass

