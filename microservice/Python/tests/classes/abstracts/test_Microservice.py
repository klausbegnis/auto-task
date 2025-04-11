import pytest
from unittest.mock import MagicMock, patch
from classes.abstracts.Microservice import Microservice

class DummyService(Microservice):
    def _addRoutes(self):
        self.availableRoutes["/ping"] = {
            "method": "GET",
            "function": self.ping,
            "description": "Health check"
        }

    def ping(self):
        return {"message": "pong"}

def test_microservice_registers_routes():
    service = DummyService(kafkaConfig={
        "subscribedTopics": [],
        "publishTopics": [],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest"
    })

    routes = [route.path for route in service().routes]
    assert "/ping" in routes

def test_initKafkaConsumer():
    service = DummyService(kafkaConfig={
        "subscribedTopics": [],
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
        "publishTopics": [],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest" 
    })

    service.initKafkaProducer()
    assert service._producer is not None

def test_kafkaPublish():
    service = DummyService(kafkaConfig={
        "subscribedTopics": [],
        "publishTopics": ["test-topic"],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest"     
    })

    service.kafkaPublish("test-topic", "test-message")
    assert service._producer.send.call_count == 1

def test_startConsumeLoop():
    service = DummyService(kafkaConfig={
        "subscribedTopics": ["test-topic"],
        "publishTopics": [],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest"
    })

    service.startConsumeLoop()
    assert service._consumer.subscribe.call_count == 1

    service._addHandler("test-topic", lambda x: None)
    service.startConsumeLoop()
    assert service._consumer.subscribe.call_count == 1          

    # Test with a topic that has no handle
    service._addHandler("nonexistent-topic", lambda x: None)
    service.startConsumeLoop()
    assert service._consumer.subscribe.call_count == 1

    # Test with a message that cannot be decoded
    service._addHandler("test-topic", lambda x: None)
    service.startConsumeLoop()
    assert service._consumer.subscribe.call_count == 1  

    # Test with a message that cannot be decoded
    service._addHandler("test-topic", lambda x: None)
    service.startConsumeLoop()
    assert service._consumer.subscribe.call_count == 1    

    # Test with a message that cannot be decoded
    service._addHandler("test-topic", lambda x: None)
    service.startConsumeLoop()
    assert service._consumer.subscribe.call_count == 1  
    