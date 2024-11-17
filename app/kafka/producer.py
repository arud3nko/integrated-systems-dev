"""This module provides `AsteroidsKafkaProducer` class"""

import json

from aiokafka import AIOKafkaProducer

from app.db.lab1 import Asteroid


class AsteroidsKafkaProducer(AIOKafkaProducer):
    """This class contains methods to produce asteroids to Kafka"""
    def __init__(self,
                 url: str,
                 topic: str):
        """
        Initialization

        :param url: Kafka bootstrap url
        :param topic: Asteroids topic
        """

        self.topic = topic
        super().__init__(bootstrap_servers=url, max_request_size=16221155)

    async def produce(self, asteroid: Asteroid):
        """
        Produce Kafka message

        :param asteroid: `Asteroid` instance to be produced to Kafka
        """

        await self.send_and_wait(
            topic=self.topic,
            value=json.dumps(
                asteroid.model_dump(mode="json")
            ).encode("utf-8"),
        )
