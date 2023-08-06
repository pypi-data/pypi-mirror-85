import asyncio
import sys
import asyncio
from rifbot.gql_queries import QUERIES, SUBSCRIPTIONS, MUTATIONS
from .GqlClient import GqlClient
from shortid import ShortId
from .SchedulerClient import SchedulerClient
from .StrategyRepositoryClient import StrategyRepositoryClient

sid = ShortId()

SERVICES = {
    'exchangeLoader': {
        'port': 8900,
        'host': 'loader.riftrading.com'
    },
    'strategyBucket': {
        'port': 8901,
    },
    'registrar': {
      'port': 9000
    },
    'authentication': {
      'port': 9001
    },
    'exchangeAccount': {
      'port': 9002
    },
    'strategyRepository': {
      'port': 9003
    },
    'scheduler': {
      'port': 9004
    },
    'exchangeLiveTickers': {
      'port': 9005
    },
    'proxy': {
      'port': 9100
    },
    'strategyRun': {
      'port': 9101,
      'range': 98
    }
}


class RifbotClient:
    def __init__(self,
                 gateway: str,
                 auth_token: str,
                 retry_count: int = 1,
                 text1: str = None,
                 text2: str = None):

        self.gateway = gateway
        self.auth_token = auth_token
        self.retry_count = retry_count
        self.connected = False
        self.dbg = 0
        self.clients = {}
        # self.nodes = {}
        self._custom_init = {
            'node': {
                'name': 'python-client',
                'id': sid.generate(),
                'text1': text1,
                'text2': text2
            }
        }

    async def scheduler(self):
        if 'scheduler' in self.clients:
            return self.clients['scheduler']

        service = await self.service('scheduler')
        client = SchedulerClient(service, self)
        self.clients['scheduler'] = client

        return client

    async def strategyRepository(self):
        if 'strategyArchive' in self.clients:
            return self.clients['strategyRepository']

        service = await self.service('strategyRepository')
        client = StrategyRepositoryClient(service, self)
        self.clients['strategyRepository'] = client

        return client

    async def service(self, name, host=None, port=None):
        if host is None:
            host = self.gateway

        if port is None:
            port = SERVICES[name]['port']

        service = GqlClient(host, port, self.auth_token, self._custom_init)

        await service.connect()
        loop = asyncio.get_event_loop()
        service.listen_coro = loop.create_task(service.listen())
        return service

    async def close(self):
        attributes = self.clients
        for k in attributes.keys():
            # print('closing', k)
            await attributes[k].close()

        await asyncio.sleep(1)

    # async def pingQuery(self):
    #     if self.connected is False: raise Exception('Use listen() first')
    #     return await self.apollo.query(QUERIES['PING'], variables={})
    #
    # async def pingSubscribe(self, callback):
    #     if self.connected is False: raise Exception('Use listen() first')
    #     subscribe_id = await self.apollo.subscribe(SUBSCRIPTIONS['PING'], callback=callback)
    #     return subscribe_id

    #
    # async def push_backtest(self, strategy, options, result_callback=None, update_callback=None):
    #     if self.connected is False: raise Exception('Use listen() first')
    #     options_json = options_to_json(options)
    #
    #     node = await self._action_node_backtest(options_json)
    #     node_id = node['id']
    #     self.nodes[node_id] = {
    #         'result': {}
    #     }
    #
    #     def subscribe_cb(raw, id):
    #         topic = raw['topic']
    #         data = raw['data']
    #         node = raw['node']
    #
    #         if topic == 'result':
    #             self.nodes[node_id]['result'].update(data)
    #             is_complete = data.get('complete') is not None
    #             # print('is_complete:', is_complete)
    #             # print('is_complete', is_complete, data.get('complete'))
    #             if is_complete is True and result_callback is not None:
    #                 result_callback(self.nodes[node_id]['result'], node_id)
    #                 del self.nodes[node_id]
    #
    #         elif topic == 'update' and update_callback is not None:
    #             update_callback(raw, node_id)
    #
    #     await self._subscribe_node(node_id, subscribe_cb)
    #     return node

    # async def get_backtest(self, id):
    #     if self.connected is False: raise Exception('Use connect() first')
    #     node = await self._query_node(id)
    #
    #     if node is None or node['id'] is None:
    #         raise Exception('Backtest id "' + str(id) + '" Not Found on the server')
    #
    #     updates = []
    #     results = []
    #     result = {}
    #
    #     for message in node['messages']:
    #         topic = message['topic']
    #         data = message['data']
    #         # print('topic:', message['topic'])
    #         if topic == 'update':
    #             updates.append(data)
    #         elif topic == 'result':
    #             results.append(data)
    #             result.update(data)
    #
    #     node['updates'] = updates
    #     node['results'] = results
    #     node['result'] = result if len(result) > 0 else None
    #
    #     return node
    #
    # async def _query_nodes(self):
    #     return await self.apollo.query(QUERIES['LIST_NODES'])
    #
    # async def _query_node(self, node_id):
    #     return await self.apollo.query(QUERIES['GET_NODE_FULL'], {
    #         'id': node_id
    #     })
    #
    # async def _subscribe_node(self, node_id, callback):
    #     return await self.apollo.subscribe(SUBSCRIPTIONS['NODE'], {
    #         'id': node_id
    #     }, callback)
    #
    # async def _action_node_backtest(self, options):
    #     return await self.apollo.mutate(MUTATIONS['ACTION_NODE'], {
    #         'nodeId': 'server-beast',  # FIXME
    #         'action': 'Backtest',
    #         'options': options
    #     })
