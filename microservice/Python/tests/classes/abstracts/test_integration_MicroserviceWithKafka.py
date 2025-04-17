import pytest
from classes.abstracts.MicroserviceWithKafka import MicroserviceWithKafka
from time import sleep
# implement integration tests

class DummyMicroservice(MicroserviceWithKafka):
    def __init__(self, kafkaConfig, host="0.0.0.0", port=8001, title="no-name-microservice", description="empty description", version="0.0.0"):
        super().__init__(kafkaConfig, host, port, title, description, version)

        self.received_messages = []

    def _addRoutes(self):
        pass
    def _addHandlers(self):
        self._registerHandlers('test-topic', self._test_topic_handler)
    
    def _test_topic_handler(self, message):
        self.received_messages.append(message)

def test_ConsumeAndPublish():
    service = DummyMicroservice(kafkaConfig={
        "subscribedTopics": ['test-topic'],
        "publishTopics": ["test-topic"],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest"     
    })
    service.startConsumeLoop()
    service.kafkaPublish("test-topic", "test-message")
    sleep(0.5)
    assert service.received_messages
    
    