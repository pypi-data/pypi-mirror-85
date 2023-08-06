import asyncio


def wait_async(func):
    # loop = asyncio.get_running_loop()
    try:
        asyncio.run(func)
    except:
        print('Using existing event loop')
        asyncio.create_task(func) #FIXME
