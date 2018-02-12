
import asyncio
import websockets
import requests
from details import ps_config as default_config 

class Client:
    """Represents a client connection that connects to PokemonShowdown.
    This class is used to interact with the PokemonShowdown WebSocket.

    """
    def __init__(self, config=None, url=None):
        self.ws = None
        # attempt connectiong to the main PS server, unless otherwise specified
        self.config = default_config if not config else config 
        self.url = 'ws://sim.psim.us:8000/showdown/websocket' if not url else url

    @asyncio.coroutine
    def start_connection(self):
        try:
            self.ws = yield from websockets.connect(self.url)
            chall_str_found = False
            while not chall_str_found:
                message = yield from self.ws.recv()
                content = message.split('|')
                if 'challstr' in message:
                    chall_str_found = True
                    challenge, challengekeyid = content[2], content[3]
                    print(challenge, challengekeyid)
                    self.login(challenge, challengekeyid)
            yield from self.ws.close()
        except:
            print('the url specified is not valid')


    @asyncio.coroutine
    def login(self, challenge, challengekeyid):
        """Logins the bot to the pokemon showdown server.
        Args:
            challenge: string, challenge key obtained from 
            challengekeyid: string,
        """
        payload = {'act': 'login',
                   'name': self.details['bot_username'],
                   'pass': self.details['bot_password'],
                   'challengekeyid': challengekeyid,
                   'challenge': challenge}
        pass


client = Client()
asyncio.get_event_loop().run_until_complete(client.start_connection())
