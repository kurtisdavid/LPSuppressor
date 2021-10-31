from lcu_driver import Connector
import time
import asyncio

connector = Connector()

@connector.ready
async def connect(connection):
    print('This script will only execute a post-game lobby exit command.')

# Exit out of post game
@connector.ws.register('/lol-honor-v2/v1/ballot', event_types=('UPDATE','CREATE','DELETE',))
async def voted(connection, event):
    if event.data is None:
        await connection.request('post', '/lol-end-of-game/v1/state/dismiss-stats')

# Exit out of Rank Up
@connector.ws.register('/lol-ranked/v1/notifications')
async def ranked_notification(connection, event):
    if event.data is not None:
        if isinstance(event.data, list) and len(event.data) > 0:
            # TODO: Figure out which ID is supposed to be used?
            #  League Client seems to close any notification if invalid (in this case we only have 1)
            await connection.request('post', f'/lol-ranked/v1/notifications/{event.data[0]}/acknowledge')
    

# starts the connector
connector.start()