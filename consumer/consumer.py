import asyncio
import logging

import aio_pika

logger = logging.getLogger(__name__)


async def consume(loop, queue_name):
    while True:
        try:
            connection = await aio_pika.connect_robust(loop=loop, host='rabbit')
        except ConnectionError:
            await asyncio.sleep(2)  # wait until rabbit starts
        else:
            break

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    logger.error(message.body.decode())


loop = asyncio.get_event_loop()
loop.run_until_complete(consume(loop, "default_queue"))
loop.close()
