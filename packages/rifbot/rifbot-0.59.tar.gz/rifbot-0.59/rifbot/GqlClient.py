import asyncio
import websockets
import json
import ssl
import sys
import string
import random

# From:
# https://pypi.org/project/py-graphql-client/
# https://pypi.org/project/websocket_client/

# Using
# https://github.com/apollographql/subscriptions-transport-ws/blob/master/PROTOCOL.md
# https://websockets.readthedocs.io/en/stable/intro.html#basic-example
##########################################
#           GRAPHQL PROTOCOL type
##########################################
# Client -> Server
GQL_CONNECTION_INIT = 'connection_init'
GQL_CONNECTION_TERMINATE = 'connection_terminate'
GQL_send_start = 'start'
GQL_send_stop = 'stop'

# Server -> Client
GQL_CONNECTION_ACK = 'connection_ack'
GQL_CONNECTION_ERROR = 'connection_error'
GQL_CONNECTION_KEEP_ALIVE = 'ka'  # NOTE: The keep alive message type does not follow the standard due to connection optimizations
GQL_DATA = 'data'
GQL_ERROR = 'error'
GQL_COMPLETE = 'complete'


class GqlClient:
    def __init__(self, host, port, authToken=None, custom_init={}):
        self.queries = {}
        self.dbg = 1
        self.uri = 'wss://' + host + ':' + str(port) + '/graphql'
        self.authToken = authToken
        self._custom_init = custom_init

    async def connect(self):
        if self.dbg >= 1: print('Connecting to', self.uri)
        # ssl._create_default_https_context = ssl._create_unverified_context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        self.ws = await websockets.client.connect(self.uri, ssl=ssl_context, subprotocols=['graphql-ws'], max_size=None)

        await self._send_init()
        res = await self._recv()
        if res['type'] != GQL_CONNECTION_ACK:
            raise ConnectionRefusedError('Cannot connect to ' + self.uri)
        elif self.dbg >= 1:
            print('Connected to', self.uri)

        # asyncio.create_task(self.listen())

    async def listen(self):
        if self.dbg >= 3: print('Listening for messages ...')
        protocol_funcs = {
            GQL_CONNECTION_ACK: self._on_connexion,
            GQL_CONNECTION_KEEP_ALIVE: self._on_connexion,
            GQL_CONNECTION_ERROR: self._on_connexion,
            GQL_DATA: self._on_data,
            GQL_COMPLETE: self._on_complete,
            GQL_ERROR: self._on_error,
        }
        self.listening = True

        while self.listening:
            try:
                message = await self._recv()
                type = message.get('type')
                payload = message.get('payload')
                id = message.get('id')

                func = protocol_funcs[type]
                if func is None:
                    print('Unknown message: ', type, payload, id)
                else:
                    func(type, payload, id)

            except websockets.ConnectionClosed as cc:
                # if self.dbg >= 1: print('Connection closed', cc)
                self.listening = False

            except BaseException as e:
                print("Listen error:", e)
                self.listening = False
                raise e

    async def query(self, query, variables=None):
        # if self.dbg >= 2: print('QUERY:', query)
        id = await self._send_start({'headers': None, 'query': query, 'variables': variables})
        resolve = asyncio.Future()
        self._push_query(id, type='query', resolve=resolve)
        await resolve
        return resolve.result()

    async def mutate(self, query, variables=None):
        # if self.dbg >= 2: print('MUTATE:', query)
        id = await self._send_start({'headers': None, 'query': query, 'variables': variables})
        resolve = asyncio.Future()
        self._push_query(id, type='mutate', resolve=resolve)
        await resolve
        return resolve.result()

    async def subscribe(self, query, variables=None, callback=None):
        # if self.dbg >= 2: print('SUBSCRIBE:', query)
        id = await self._send_start({'headers': None, 'query': query, 'variables': variables})
        self._push_query(id, 'subs', callback=callback)
        return id

    def stop_subscribe(self, id):
        # if self.dbg >= 4: print('stop_subscribe:', id)
        asyncio.create_task(self._send_stop(id))

    def close(self):
        # if self.dbg >= 1: print('Connection closing')
        asyncio.create_task(self.ws.close())

    def _push_query(self, id, type, resolve=None, callback=None):
        q = {
            'type': type,
            'result': None,
            'resolve': resolve,
            'callback': callback,
            'error': None
        }
        # if self.dbg >= 3: print('CREATE Query:', id, str(q))
        self.queries[id] = q

    def _del_query(self, id):
        q = self.queries[id]
        # if self.dbg >= 3: print('DELETE Query:', id, str(q))
        del self.queries[id]

    async def _send_init(self):
        payload = {
            'authToken': self.authToken
        }
        payload.update(self._custom_init)

        await self._send({
            'type': 'connection_init',
            'payload': payload
        })

    async def _send_start(self, payload):
        id = gen_id()
        await self._send({'id': id, 'type': GQL_send_start, 'payload': payload})
        return id

    async def _send_stop(self, id):
        await self._send({'id': id, 'type': GQL_send_stop})

    def _on_connexion(self, type, payload, id):
        if self.dbg >= 4: print("_on_connexion:", type, payload, id)

    def _on_data(self, type, payload, id):
        # if self.dbg >= 4:
        # print('_on_data ', id, type, payload, 'errors:', payload.get('errors') is not None)

        has_errors = payload.get('errors') is not None
        if has_errors:
            raise Exception('Message has errors: ' + str(payload.get('errors')))

        query = self.queries[id]
        if query is None:
            print('Unknown query: ' + id)
        else:
            if query['type'] == 'query' or query['type'] == 'mutate':
                if query['result'] is not None:
                    print('WARN: Result not none: ' + str(query['result']))
                # if self.dbg >= 4: print('_on_data ' + id + ' set result to: ' + str(payload))
                keys = list(payload['data'].keys())
                query['result'] = res = payload['data'].get(keys[0])
            elif query['type'] == 'subs':
                # if self.dbg >= 2: print('SUBSCRIPTION', id, payload)
                cb = query['callback']
                if payload.get('errors') is not None:
                    print('Error in subscription', id, payload.get('errors'))
                keys = list(payload['data'].keys())
                res = payload['data'].get(keys[0])
                # cb(res, id)
                cb(res)

    def _on_complete(self, type, payload, id):
        # if self.dbg >= 4: print("_on_complete:", type, payload, id)
        query = self.queries[id]
        if query is None:
            print('Unknown query: ' + id)
        else:
            if query['type'] == 'query' or query['type'] == 'mutate':
                # if self.dbg >= 4: print('_on_complete ' + id + ' resolve - result: ' + str(query['result']))
                query['resolve'].set_result(query['result'])

        self._del_query(id)

    def _on_error(self, type, payload, id):
        print("_on_error:", type, payload, id)

    async def _recv(self):
        res = await self.ws.recv()
        parsed = json.loads(res)
        # print('_recv', str(parsed))
        return parsed

    async def _send(self, data):
        # print('_send', data)
        jsonValue = json.dumps(data)
        await self.ws.send(jsonValue)


# generate random alphanumeric id
def gen_id(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
