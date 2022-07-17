import os
import uuid
import logging
import json
from typing import Callable

import pika

## Configure logger
FORMAT = "%(levelname)s:\t [%(asctime)s] [%(message)s]" 
logging.basicConfig(level=logging.INFO, format=FORMAT)

USER = os.environ.get('RABBIT_USER')
PASS = os.environ.get('RABBIT_PASSWORD')
HOST = os.environ.get('RABBIT_HOST')
PORT = os.environ.get('RABBIT_PORT')
QUEUE = os.environ.get('RABBIT_QUEUE')

credentials = pika.PlainCredentials(USER, PASS)

class RabbitMQAgent(object):

    '''
    A class to implement communication with the rabbitmq
    message broker using an RPC request/reply pattern.

    > Inspiration taken from here:
s        - https://itracer.medium.com/rabbitmq-publisher-and-consumer-with-fastapi-175fe87aefe1
    '''

    def __init__(self, message_handler: Callable):

        '''
        Initialise a new connection to the message broker
        '''

        # Define class attrs
        self.message_handler = message_handler # Function to process worker response
        self.response = None
        self.corr_id = None

        # Set up RabbitMQ Connection
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=HOST,
                port=PORT,
                credentials=credentials
            )
        )

        # Set up channel
        self.channel = self.connection.channel()

        # Create a queue
        q_name = QUEUE+'-'+str(uuid.uuid4())[:4]
        queue = self.channel.queue_declare(queue=q_name, exclusive=True)

        # Capture the address of the queue that will contain responses
        self.return_address = queue.method.queue

        # Create a consume connection to listen to responses
        self.channel.basic_consume(
            queue = self.return_address,
            on_message_callback = self._on_response,
            auto_ack = True,
        )

        logging.info(f'CLIENT: new connection created {HOST}:{PORT} channel={q_name}')

    
    def send_message(self, message: dict) -> None:
        '''
        '''

        # Reinitialise the state
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # Send the request
        self.channel.basic_publish(

            exchange = '',
            routing_key = 'rpc_queue',

            properties = pika.BasicProperties(

                reply_to = self.return_address,
                correlation_id = self.corr_id,

            ),

            body = json.dumps(message)
        )

        logging.info(f'CLIENT: message sent: {self.corr_id}')

        self.connection.process_data_events(time_limit=None)

        return self.response

    
    def _on_response(self, ch, method, props, body) -> None:
        '''
        '''
        
        if self.corr_id == props.correlation_id:

            # Parse response and stash results
            self.response = self.message_handler(body)

            logging.info(f'CLIENT: message recieved: {props.correlation_id}')

