from lcu_driver import Connector
import time
import asyncio

connector = Connector()

@connector.ready
async def connect(connection):
    print('This script will only execute a post-game lobby exit command.')

@connector.ws.register('/lol-honor-v2/v1/ballot', event_types=('UPDATE','CREATE','DELETE',))
async def voted(connection, event):
    if event.data is None:
        await connection.request('post', '/lol-end-of-game/v1/state/dismiss-stats')

# starts the connector
connector.start()