import asyncio
from rifbot import GqlClient, RootOptions, RifbotClient
from rifbot.gql_queries import QUERIES, SUBSCRIPTIONS, MUTATIONS
from shortid import ShortId
import json
import pprint
import time

pp = pprint.PrettyPrinter(indent=4)


class SchedulerClient:
    def __init__(self, service: GqlClient, root: RifbotClient):
        # print('SchedulerClient')
        self.root = root
        self.service = service

    async def enqueueStrategyRun1(self, rootOptions: RootOptions, runId: str = None):
        if runId is None:
            runId = ShortId().generate()

        return await self.service.mutate(MUTATIONS['ENQUEUE_STRATEGY_RUN'], {
            'rootOptions': rootOptions.__dict__,
            'runId': runId,
        })

    sub = None
    async def callOnEnd(job):
        runId = job['executor']['id']
        strategyRepository = await self.root.strategyRepository()
        runResult = await strategyRepository.findOneStrategyResult(runId)
        self.service.stop_subscribe(sub)
        onEnd(runResult)

    sub = await self.onJobFinished(
        listener=lambda j: asyncio.get_event_loop().create_task(callOnEnd(j)),
        jobId=runId,
    )

    async def onJobStarted(self, listener=None, jobId=None):
        return await self.service.subscribe(
            query=SUBSCRIPTIONS['ON_JOB_STARTED'],
            variables={
                'jobId': jobId,
            },
            callback=listener
        )

    async def onJobFinished(self, listener=None, jobId=None):
        return await self.service.subscribe(
            query=SUBSCRIPTIONS['ON_JOB_FINISHED'],
            variables={
                'jobId': jobId,
            },
            callback=listener
        )

    async def close(self):
        self.service.close()
        self.service.listen_coro.cancelled()
