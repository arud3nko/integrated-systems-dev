import asyncio
import json

import httpx

from threading import Thread

from loguru import logger
from aiokafka import AIOKafkaConsumer

from models import AsteroidSchema


SERVER_URL = "http://127.0.0.1:8081"

LAST_ASTEROID_ID = None


def parse_input():
    while True:
        _ = input()

        client = httpx.Client()

        if LAST_ASTEROID_ID is None:
            print("Еще не было получено информации об астероидах")
            continue

        resp = client.get(url=SERVER_URL + f"/lab2/asteroids/{LAST_ASTEROID_ID}/")

        asteroid = AsteroidSchema.model_validate(resp.json())

        print("Подробная информация о последнем астероиде")

        for key, value in asteroid.dict().items():
            print(f"{key.upper()} | {value}")


async def main():
    global LAST_ASTEROID_ID

    consumer = AIOKafkaConsumer(
    "asteroids",
        bootstrap_servers='localhost:29092'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            value = json.loads(msg.value)
            asteroid = AsteroidSchema.model_validate(value)
            logger.info(f"Получена информация о новом астероиде\n"
                        f"Наименование: {asteroid.designation}\n"
                        f"Дата открытия: {asteroid.discovery_date}")
            LAST_ASTEROID_ID = value.get("id")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    client_task = Thread(target=parse_input)
    client_task.start()

    print("Нажмите ENTER для получения подробной информации о последнем астероиде\n")

    asyncio.run(main())
