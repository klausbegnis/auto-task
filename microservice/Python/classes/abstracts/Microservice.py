from fastapi import FastAPI, HTTPException, Request
import uvicorn
import logging
from datetime import datetime
from abc import ABC, abstractmethod
import jwt
import json
from jwt import InvalidTokenError

class Microservice(ABC):
    def __init__(self, host="0.0.0.0", port=8001, title="no-name-microservice", description="empty description", version="0.0.0"):
        
        """
        Initialize the Microservice
        """
        
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Initializing the Microservice")

        # API description
        self.title = title
        self.description = description
        self.version = version

        # API configuration
        # Port configuration
        self.port = port
        self.host = host
        # Initialize the FastAPI app
        self._api = FastAPI(title=self.title, description=self.description, version=self.version)
        
        # Available routes for the API
        # "endpoint" : {
        #     "method": "GET",
        #     "function": self.function,
        #     "description": "Description of the endpoint"
        #
        # Used to register the routes to the FastAPI app
        #
        # _addRoutes() is used to fill the availableRoutes dictionary
        # -> this function is implemented by the child class
        
        self.availableRoutes = {}     

        self._addRoutes() # -> fill the availableRoutes dictionary
        self._requestRegister() # -> register the routes to the FastAPI app
    
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Microservice initialized")

    def __call__(self):
        """
        Return the FastAPI app  
        """
        return self._api

    @abstractmethod
    def _addRoutes(self):
        """
        Add the routes to the FastAPI app
        """
        pass

    def _requestRegister(self):
        """
        Register the API endpoints
        """

        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Registering the API endpoints")

        # Register the API endpoints

        if not self.availableRoutes:
            logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - No API endpoints to register")
            return

        try:
            for endpoint, config in self.availableRoutes.items():
                self._api.add_api_route(
                    path=endpoint,
                    endpoint=config["function"],
                    methods=[config["method"]],
                    description=config["description"]
                )
        except Exception as e:
            logging.error(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Error while registering the API endpoints: " + str(e))

    def run(self):
        """
        Run the FastAPI app
        """
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - API is running on " + self.host + ":" + str(self.port))

        try:    
            uvicorn.run(self._api, host=self.host, port=self.port)

        except Exception as e:
            logging.error(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Error while running the FastAPI app: " + str(e))

    def _validate_internal_jwt(self, request: Request, secret_key: str = None):
        """
        Validates the JWT provided in the Authorization header of the request.
        """
        # Get Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f"[Microservice] - missing authorization header {request}")
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

        token = auth_header.split(" ")[1]

        try:
            # Decode the JWT
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except InvalidTokenError as e:
            logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f"[JWT ERROR] {e}")
            raise HTTPException(status_code=403, detail="Invalid or expired token")
    
    def _load_internal_jwt_key(self):
        with open("./secrets/internal_secret_key.json") as f:
            return json.load(f)['secret_key']