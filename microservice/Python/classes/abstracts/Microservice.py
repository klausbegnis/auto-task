from fastapi import FastAPI
from kafka import KafkaConsumer, KafkaProducer
import threading
import uvicorn
import logging
import json
from time import time
from datetime import datetime
from abc import ABC, abstractmethod

class Microservice(ABC):
    def __init__(self, kafkaConfig, host="0.0.0.0", port=8000, title="no-name-microservice", description="empty description", version="0.0.0"):
        
        """
        Initialize the Microservice
        """
        
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Initializing the Microservice")

        # API description
        self.title = title
        self.description = description
        self.version = version

        # Kafka configuration
        self.subscribedTopics = kafkaConfig["subscribedTopics"]
        self.publishTopics = kafkaConfig["publishTopics"]

        self._kafkaConfig = {
            "bootstrap.servers": kafkaConfig["bootstrap.servers"]   ,
            "group.id": kafkaConfig["group.id"],
            "auto.offset.reset": kafkaConfig["auto.offset.reset"]
        }

        # Kafka consumer and producer 
        self._consumer = None
        self._producer = None

        # Kafka consume thread
        self._consume_thread = None

        # Topic handlers
        # Used to link each topic to a message handler
        # {
        #     "topic": {
        #         "handler": self.handler
        #     }
        # }
        self._topic_handlers = {}

        # API configuration
        # Port configuration
        self.port = port
        self.host = host
        # Initialize the FastAPI app
        self._api = FastAPI(title=self.title, description=self.description, version=self.version)
        self._unicorn_server = None
        self._uvicorn_thread = None
        
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

    def shutdown(self):
        """
        Close all connections from Microservice 
        (__del__) garbage collector already delete a few elements
        Use this function on the end of lifetime for extra safety
        """
        try:

            logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Destroying Microservice instance")
            # check if the consumer and producer are not none
            # and close them
            if self._consumer:
                self._consumer.close()
                self._consume_thread = None
                logging.info("Kafka consumer closed")

            if self._producer:
                self._producer.close()
                logging.info("Kafka producer closed")

            # closes the API server
            if self._uvicorn_server and self._uvicorn_server.should_exit is False:
                self._uvicorn_server.should_exit = True
                timedOut = False
                time_out_seconds = 30
                test_interval = 0.1
                wait_counter = 0
                # constantly checks if the uvicorn server closed correctly
                while self._uvicorn_thread.is_alive() and not(timedOut):
                    time.sleep(test_interval)
                    wait_counter += test_interval
                    if test_interval >= time_out_seconds:
                        timedOut = True
                
                if timedOut:
                    logging.warning("Uvicorn server exit timedout, proceeding to kill thread directly.")

                self._uvicorn_thread.join()
                logging.info("Uvicorn server stopped")

        except Exception as e:
            logging.warning(f"Exception during shutdown: {e}")

    @abstractmethod
    def _addRoutes(self):
        """
        Add the routes to the FastAPI app
        """
        pass

    def _addHandler(self, topic, handler):
        """
        Add a handler to a topic
        """
        self._topic_handlers[topic] = handler

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
            # Run the FastAPI app
            self._unicorn_server = uvicorn.Server(self._api, host=self.host, port=self.port)
            self._uvicorn_thread = threading.Thread(target=self._uvicorn_server.run, daemon=True)
            self._uvicorn_thread.start()

        except Exception as e:
            logging.error(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Error while running the FastAPI app: " + str(e))
    
    def initKafkaConsumer(self):
        """
        Initialize the Kafka consumer
        """

        
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Initializing the Kafka consumer")
        
        try:
            self._consumer = KafkaConsumer(
                *self.subscribedTopics,
                bootstrap_servers=self._kafkaConfig["bootstrap.servers"],
                group_id=self._kafkaConfig["group.id"],
                auto_offset_reset=self._kafkaConfig["auto.offset.reset"]
            )      
            logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Kafka consumer initialized")
        except Exception as e:
            logging.error(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Error while initializing the Kafka consumer: " + str(e))
    
    def initKafkaProducer(self):
        """
        Initialize the Kafka producer
        """

        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Initializing the Kafka producer")

        try:
            self._producer = KafkaProducer(
                bootstrap_servers=self._kafkaConfig["bootstrap.servers"]
            )
            logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Kafka producer initialized")
        except Exception as e:
            logging.error(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Error while initializing the Kafka producer: " + str(e))
    
    def startConsumeLoop(self):
        """
        Start the consume loop
        """

        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Starting the consume loop")

        # Initialize the Kafka consumer if it is not initialized
        if not self._consumer:
            self.initKafkaConsumer()

        # Start the consume loop
        try:
            self._consume_thread = threading.Thread(target=self.consumeLoop, daemon=True)
            self._consume_thread.start()
        except Exception as e:
            logging.error(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Raised exception while starting the consume thread: " + str(e))
    
    def consumeLoop(self):
        """
        Consume loop
        """
        
        # Consume messages from the Kafka topics
        for message in self._consumer:
            try:
                self.handleConsumedMessage(message.topic, message.value.decode("utf-8"))
            except Exception as e:
                logging.error(f"Raised exception while handling the consume message: " + str(e))
    
    def kafkaPublish(self, topic, message: str | bytes):
        """
        Publish a message to a Kafka topic
        """

        # Initialize the Kafka producer if it is not initialized
        if not self._producer:
            self.initKafkaProducer()

        # Publish the message to the Kafka topic    
        try:
            if isinstance(message, str):
                message = json.dumps(message)
            self._producer.send(topic, message.encode("utf-8"))
        except Exception as e:
            logging.error(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Raised exception while publishing the message to the Kafka topic: " + str(e)) 
    
    def handleConsumedMessage(self, topic, message):
        """
        Handle a message from a Kafka topic
        """
        
        # Get the handler for the topic
        try:
            handler = self._topic_handlers[topic]
        except Exception as e:
            logging.warning(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Topic: " + topic + " with no topic handler")
            return

        # Call the handler
        handler(message)
