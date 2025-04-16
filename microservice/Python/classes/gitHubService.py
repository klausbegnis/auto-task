from abstracts.Microservice import Microservice
from time import sleep
class GitHubService(Microservice):
    def __init__(self, kafkaConfig, host="0.0.0.0", port=8001, title="github-service", description="Microservice to handle communication with github", version="0.0.1"):
        super().__init__(kafkaConfig, host, port, title, description, version)
    
        self.run()
    def _addRoutes(self):
            self.availableRoutes['/'] = {
                "method" : "GET",
                "function" : self._im_alive,
                "description" : "Health check"
        }
    

    def _im_alive(self):
        return True

if __name__ == '__main__':
    test = GitHubService(kafkaConfig={
        "subscribedTopics": [],
        "publishTopics": ["test-topic"],
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest"     
    })

