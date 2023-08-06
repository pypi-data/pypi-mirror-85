from rifbot import GqlClient, RifbotClient
from rifbot.gql_queries import QUERIES, SUBSCRIPTIONS, MUTATIONS
from shortid import ShortId


class StrategyRepositoryClient:
    def __init__(self, service: GqlClient, root: RifbotClient):
        # print('StrategyRepositoryClient')
        self.root = root
        self.service = service

    async def findOneStrategyResult(self, runId:str):
        # print('findOneStrategyResult', 'runId:', runId)

        res = await self.service.query(QUERIES['FIND_ONE_STRATEGY_RESULT'], {
            'runId': runId
        })

        return res


    async def findStrategyOrdersResult(self, runId:str):
        # print('findOneStrategyResult', 'runId:', runId)

        res = await self.service.query(QUERIES['FIND_STRATEGY_ORDERS_RESULT'], {
            'runId': runId
        })

        return res


    async def close(self):
        self.service.close()
        self.service.listen_coro.cancelled()
