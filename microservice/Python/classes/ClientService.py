from classes.abstracts.Microservice import Microservice
from fastapi import Request
from classes.dataModels.data_models import UserLogin, CreateUser
import json
import logging

class ClientService(Microservice):
    def __init__(self, host="0.0.0.0", port=8010, title="client-service", description="Microservice fo client authentication", version="0.0.1"):
        super().__init__(host, port, title, description, version)
        self.__secret_key_internal = self._load_internal_jwt_key()
    
    def _addRoutes(self):
        self.availableRoutes['/'] = {
            "method" : "GET",
            "function" : self._im_alive,
            "description" : "Health check"
        }   
        self.availableRoutes['/register'] = {
            "method" : "POST",
            "function" : self._register,
            "description" : "Create new user."
        }
        self.availableRoutes['/login']= {
            "method" : "POST",
            "function" : self._login,
            "description" : "Login the user."
        }

    
    def _im_alive(self):
        return True
    
    def _register(self, credentials: CreateUser):

        username = credentials.username
        password = credentials.password
        email = credentials.email

        # encrypt and save
        return {"user" : username}
    
    def _login(self, user_data: UserLogin):
        pass
    
    def create_session_cookie(self):
        pass
