from typing import Dict, Optional
import json

from fastapi import FastAPI
from pydantic import BaseModel
import aio_pika

app = FastAPI()


async def publish(message, routing_key):
    connection = await aio_pika.connect_robust(host='rabbit')
    channel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message, default=dict).encode()
        ),
        routing_key=routing_key
    )

    await connection.close()


class Message(BaseModel):
    taskid: str
    title: str
    params: Optional[Dict[str, str]] = None


@app.post("/tasks/")
async def add_task(message: Message, routing_key: str = "default_queue"):
    await publish(message, routing_key)

    return message
