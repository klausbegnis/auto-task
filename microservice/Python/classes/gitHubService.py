from microservice.Python.classes.abstracts.Microservice import Microservice
class GitHubService(Microservice):
    def __init__(self, host="0.0.0.0", port=8001, title="github-service", description="Microservice to handle communication with github", version="0.0.1"):
        super().__init__(host, port, title, description, version)
    
        self.run()
    def _addRoutes(self):
            self.availableRoutes['/'] = {
                "method" : "GET",
                "function" : self._im_alive,
                "description" : "Health check"
        }
    

    def _im_alive(self):
        return True


