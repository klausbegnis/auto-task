from classes.abstracts.Microservice import Microservice
import json
import requests
import logging
from datetime import datetime
from fastapi import Request, HTTPException

class GitHubService(Microservice):
    def __init__(self, host="0.0.0.0", port=8010, title="github-service", description="Microservice to handle communication with github", version="0.0.1"):
        super().__init__(host, port, title, description, version)
        
        self._git_api_url = "https://api.github.com/"
        self.__secret_key_internal = self._load_internal_jwt_key() # to communicate using jwt with other services

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
        self.availableRoutes['/save-token']= {
            "method" : "POST",
            "function" : self._save_token,
            "description" : "Saves the user token."
        }

    def _load_token(self, user):
        """
        Loads the saved token from a user:

        Params:
            user [str]
        
        Returns:
            token [str]
        """
        with open('/home/token_bearer.json') as token_file: # change this to use database in the future
            try:
               return(json.load(token_file)[user]["token"])
            except:
                logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Failed to retrieve user's token.")
                return


    def _im_alive(self):
        """
        Health check!

        Returns:
            True [bool]
        """
        return True

    def _list_reps(self, request: Request):
        """
        List all repositories from user.

        Params:
            Request [PyDantic]
                {jwt encoded bearer token} -> contains "sub" key with username
        
        Returns:
            JSON Response [list]
        """
        payload = self._validate_internal_jwt(request, secret_key=self.__secret_key_internal)
        user = payload.get("sub")
        if not user:
            logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " [/list-reps]- User id not mentioned in token.")
            raise HTTPException(status_code=400, detail="Missing 'sub' in token payload")
        git_token = self._load_token(user=user)
        header = self._create_headers(token=git_token)
        endpoint = f"users/{user}/repos"
        response = requests.get(self._git_api_url + endpoint, headers=header)

        return response.json()

    def _save_token(self, request: Request):
        """
        Saves the GitHub token from a user:

        Params:
            Request [PyDantic]
                {jwt encoded bearer token} -> 
                    {
                        sub : [str],
                        git_token: [str]
                    }
        Returns:
            HTTPStatusCode
        
        """
        payload = self._validate_internal_jwt(request, secret_key=self.__secret_key_internal)
        user = payload.get("sub")
        if not user:
            logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " [/list-reps]- User id missing in token.")
            raise HTTPException(status_code=400, detail="Missing 'sub' in token payload")
        token = payload.get("git_token")
        if not token:
            logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" [/list-reps]- User token for {user} missing in payload.")
            raise HTTPException(status_code=400, detail="Missing 'token' in request payload")
        try:
            self._store_token(user, token)
        except:
            logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" [/list-reps]- failed to save token for user: {user}.")
            raise HTTPException(status_code=400, detail=f"Failed to save token for user: {user}")
        return {"message": "Token saved successfully", "user": user}

    def _store_token(self, user, token):

        """
        Stores the user and token into the DB.

        Params:
            user : [str]
            token : [str]
        """

        file_path = '/home/token_bearer.json'

        try:
            # Load existing tokens
            with open(file_path, 'r') as token_file:
                data = json.load(token_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Add or update token for the user
        data[user] = {"token": token}

        # Write back to the file
        with open(file_path, 'w') as token_file:
            json.dump(data, token_file, indent=4)
