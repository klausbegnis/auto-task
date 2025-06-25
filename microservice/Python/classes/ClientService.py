from classes.abstracts.Microservice import Microservice
from fastapi import Request
import json
import logging

class ClientService(Microservice):
    def __init__(self, host="0.0.0.0", port=8010, title="client-service", description="Microservice fo client authentication", version="0.0.1"):
        super().__init__(host, port, title, description, version)
        self.__secret_key_internal = "123ua8sd9123h1k!@#!K$1j" # to communicate using jwt with other services
    
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
    
    async def _register(self, request: Request):
        data = await request.json()

        user = data.get("user")
        password = data.get("password")
        email = data.get("email")

        # encrypt and save - return webcookie with session token

        return {"user" : data.get("user")}
    
    def _login(self, request: Request):
        pass
    
    def create_session_cookie(self):
        pass
