from microservice.Python.classes.abstracts.MicroserviceWithKafka import MicroserviceWithKafka

# implement integration tests

class DummyMicroservice(MicroserviceWithKafka):
    def _addRoutes(self):
        pass
    def _addHandlers(self):
        pass

def test_ConsumeAndPublish():
    service = MicroserviceWithKafka(kafkaConfig={
        "subscribedTopics": ['test-topic'],
        "publishTopics": ["test-topic"],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest"     
    })
    service.startConsumeLoop()
    service.kafkaPublish("test-topic", "test-message")
    
    