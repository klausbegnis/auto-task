from classes.abstracts.Microservice import Microservice

# implement integration tests

def test_kafkaPublish():
    service = Microservice(kafkaConfig={
        "subscribedTopics": [],
        "publishTopics": ["test-topic"],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest"     
    })

    service.kafkaPublish("test-topic", "test-message")
    