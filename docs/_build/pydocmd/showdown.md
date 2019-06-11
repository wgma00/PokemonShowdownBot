<h1 id="showdown.Client">Client</h1>

```python
Client(self, config=None, url=None, log_errors=False)
```
Represents a client connection that connects to PokemonShowdown.

This class handles the major client-side connection to the PokemonShowdown
server. It also provides an API wrapper for the basic PS commands and
protocols PS abides by.

You should expect to be somewhat familiar with the PS protocols outlined below:
https://github.com/Zarel/Pokemon-Showdown/blob/master/PROTOCOL.md
if you want to make edits to the following piece of code.

For the sake of simplicity, we assume that the command char used is ~ in
the documentation.

Attributes:
    ws: websockets connection, asyncio compliant websocket client.
    rooms: map of Room, map containing all of the rooms this bot is in.
    config: dict, contains all relevant config details for the bot.
    session: session, coroutine session required for aiohttp connections.
    log_errors: bool, whether or not to log exceptions.

