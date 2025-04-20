from abstracts.MicroserviceWithKafka import MicroserviceWithKafka
import json
import requests
import logging
from datetime import datetime

class GitHubService(MicroserviceWithKafka):
    def __init__(self, host="0.0.0.0", port=8010, title="github-service", description="Microservice to handle communication with github", version="0.0.1"):
        super().__init__(host, port, title, description, version)
        
        self._git_api_url = "https://api.github.com/"
        self.run()

    def _create_headers(self, token):
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def _addRoutes(self):
        self.availableRoutes['/'] = {
            "method" : "GET",
            "function" : self._im_alive,
            "description" : "Health check"
        }   
        self.availableRoutes['/list-reps'] = {
            "method" : "GET",
            "function" : self._list_reps,
            "description" : "List all repositories available for the organization."
        }

    def _load_token(self, user):
        with open('./token_bearer.json') as token_file: # change this to use database in the future
            try:
               return(json.load(token_file)[user]["token"])
            except:
                logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Failed to retrieve user's token.")
                return


    def _im_alive(self):
        return True

    def _list_reps(self):
        test_user = "klausbegnis"
        token = self._load_token(user=test_user)
        header = self._create_headers(token=token)

        endpoint = f"users/{test_user}/repos"
        response = requests.get(self._git_api_url+endpoint, headers=header)
        return(response.json())



if __name__ == '__main__':
    service = GitHubService()