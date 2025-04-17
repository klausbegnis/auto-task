import pytest
#from unittest.mock import MagicMock, patch
from classes.abstracts.MicroserviceWithKafka import MicroserviceWithKafka

class DummyService(MicroserviceWithKafka):
    def _addRoutes(self):
        pass
    def _addHandlers(self):
        self._registerHandlers('test-topic', self._test_topic_handler)
    def _test_topic_handler(self):
        pass

def test_microservice_registers_routes():
    service = DummyService(kafkaConfig={
        "subscribedTopics": ['test-topic'],
        "publishTopics": [],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest"
    })
    print(service._topic_handlers)
    assert 'test-topic'in service._topic_handlers.keys()

def test_initKafkaConsumer():
    service = DummyService(kafkaConfig={
        "subscribedTopics": ['test-topic'],
        "publishTopics": [],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest"
    })

    service.initKafkaConsumer()
    assert service._consumer is not None

def test_initKafkaProducer():
    service = DummyService(kafkaConfig={
        "subscribedTopics": [],
        "publishTopics": ['test-topic'],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest" 
    })

    service.initKafkaProducer()
    assert service._producer is not None
