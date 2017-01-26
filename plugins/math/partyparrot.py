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

try:
    from plugins.math.images import OnlineImage
except ImportError:
    from images import OnlineImage

import random

class PartyParrot(OnlineImage):
    _Base = 'http://cultofthepartyparrot.com/parrots/' 
    _Parrot = { 'aussiecongaparrot':'.gif', 'aussieparrot':'.gif',
                'aussiereversecongaparrot':'.gif', 'bananaparrot':'.gif',
                'blondesassyparrot':'.gif', 'bluecluesparrot':'.gif',
                'bluescluesparrot':'.gif', 'boredparrot':'.gif',
                'chillparrot':'.gif', 'christmasparrot':'.gif',
                'coffeeparrot':'.gif', 'confusedparrot':'.gif',
                'congaparrot':'.gif', 'congapartyparrot':'.gif', 
                'darkbeerparrot':'.gif', 'dealwithitparrot':'.gif', 
                'dreidel-parrot':'.xcf', 'dreidelparrot':'.gif',
                'driedelparrot':'gif', 'driedelparrot2':'.gif',
                'explodyparrot':'.gif', 'fastparrot':'.gif', 'fieriparrot':'.gif',
                'fiestaparrot':'.gif', 'gentlemanparrot':'.gif', 'gothparrot':'.gif',
                'halalparrot':'.gif', 'hamburgerparrot':'.gif',
                'harrypotterparrot':'.gif', 'ice-cream-parrot':'.gif',
                'magaritaparrot':'.gif', 'margaritaparrot':'.gif', 'middleparrot':'.gif',
                'moonwalkingparrot':'.gif', 'oldtimeyparrot':'.gif',
                'oriolesparrot':'.gif', 'parrot':'.gif', 'parrotbeer':'.gif',
                'parrotcop':'.gif', 'parrotdad':'.gif', 'parrotmustache':'.gif',
                'parrotsleep':'.gif', 'parrotwave1':'.gif', 'parrotwave2':'.gif',
                'parrotwave3':'.gif', 'parrotwave4':'.gif', 'parrotwave5':'.gif',
                'parrotwave6':'.gif', 'parrotwave7':'.gif', 'partyparrot':'.gif',
                'pizzaparrot':'.gif', 'reversecongaparrot':'.gif', 'rightparrot':'.gif',
                'sadparrot':'.gif', 'sassyparrot':'.gif', 'shipitparrot':'.gif',
                'shufflefurtherparrot':'.gif', 'shuffleparrot':'.gif', 
                'shufflepartyparrot':'.gif', 'skiparrot':'.gif', 'slowparrot':'.gif',
                'stableparrot':'.gif', 'tripletsparrot':'.gif', 'twinsparrot':'.gif',
                'upvotepartyparrot':'.gif', 'witnessprotectionparrot':'.gif', 
                'aussiecongaparrot':'.gif', 'aussieparrot':'.gif', 
                'aussiereversecongaparrot':'.gif', 'bananaparrot':'.gif', 
                'blondesassyparrot':'.gif', 'bluecluesparrot':'.gif',
                'bluescluesparrot':'.gif', 'boredparrot':'.gif', 'chillparrot':'.gif',
                'christmasparrot':'.gif', 'coffeeparrot':'.gif', 'confusedparrot':'.gif',
                'congaparrot':'.gif', 'congapartyparrot':'.gif', 'darkbeerparrot':'.gif',
                'dealwithitparrot':'.gif', 'dreidel-parrot':'.xcf', 
                'dreidelparrot':'.gif', 'driedelparrot':'.gif', 'driedelparrot2':'.gif',
                'explodyparrot':'.gif', 'fastparrot':'.gif', 'fieriparrot':'.gif',
                'fiestaparrot':'.gif', 'gentlemanparrot':'.gif', 'gothparrot':'.gif',
                'halalparrot':'.gif', 'hamburgerparrot':'.gif', 
                'harrypotterparrot':'.gif', 'ice-cream-parrot':'.gif', 
                'magaritaparrot':'.gif', 'margaritaparrot':'.gif', 'middleparrot':'.gif',
                'moonwalkingparrot':'.gif', 'oldtimeyparrot':'.gif', 
                'oriolesparrot':'.gif', 'parrot':'.gif', 'parrotbeer':'.gif',
                'parrotcop':'.gif', 'parrotdad':'.gif', 'parrotmustache':'.gif',
                'parrotsleep':'.gif', 'parrotwave1':'.gif', 'parrotwave2':'.gif',
                'parrotwave3':'.gif', 'parrotwave4':'.gif', 'parrotwave5':'.gif',
                'parrotwave6':'.gif', 'parrotwave7':'.gif', 'partyparrot':'.gif',
                'pizzaparrot':'.gif', 'reversecongaparrot':'.gif', 'rightparrot':'.gif',
                'sadparrot':'.gif', 'sassyparrot':'.gif', 'shipitparrot':'.gif',
                'shufflefurtherparrot':'.gif', 'shuffleparrot':'.gif',
                'shufflepartyparrot':'.gif', 'skiparrot':'.gif', 'slowparrot':'.gif',
                'stableparrot':'.gif', 'tripletsparrot':'.gif', 'twinsparrot':'.gif',
                'upvotepartyparrot':'.gif', 'witnessprotectionparrot':'.gif'}

    @staticmethod
    def random_parrot():
        parrot = random.choice(list(PartyParrot._Parrot.keys())) 
        ext = PartyParrot._Parrot[parrot]
        url = PartyParrot._Base +  parrot + ext 
        return url, PartyParrot.get_image_info(url) 

    @staticmethod
    def get_parrot(parrot):
        if parrot in PartyParrot._Parrot:
            parrot, ext = parrot, PartyParrot._Parrot[parrot] 
            url = PartyParrot._Base +  parrot + ext 
            return url, PartyParrot.get_image_info(url) 
        return None



print(PartyParrot.random_parrot())
print(PartyParrot.get_parrot('congapartyparrot'))
