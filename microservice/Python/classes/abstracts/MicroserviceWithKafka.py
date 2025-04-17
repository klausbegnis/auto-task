from kafka import KafkaConsumer, KafkaProducer
import threading
import uvicorn
import logging
import json
from datetime import datetime
from abc import abstractmethod
from classes.abstracts.Microservice import Microservice

class MicroserviceWithKafka(Microservice):
    def __init__(self, kafkaConfig, host="0.0.0.0", port=8001, title="no-name-microservice", description="empty description", version="0.0.0"):
        """
        Initialize the Microservice
        """
        super().__init__(host=host, port=port, title=title, description=description, version=version)

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
        self._addHandlers()

    def shutdownKafka(self):
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

        except Exception as e:
            logging.warning(f"Exception during shutdown: {e}")

    @abstractmethod
    def _addHandlers(self):
        """
        Add the handlers to the subscribed topics
        """
        pass

    def _registerHandlers(self, topic, handler):
        """
        Register the handlers
        """
        self._topic_handlers[topic] = handler

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
