import os
import json
import logging

import pika

from database.dependencies import get_db
from database.crud import get_metadata
from database.schemas import ClientRequest

USER = os.environ.get('RABBIT_USER')
PASS = os.environ.get('RABBIT_PASSWORD')
HOST = os.environ.get('RABBIT_HOST')
PORT = os.environ.get('RABBIT_PORT')
QUEUE = os.environ.get('RABBIT_QUEUE')

## Configure logger
FORMAT = "%(levelname)s:\t [%(asctime)s] [%(message)s]" 
logging.basicConfig(level=logging.ERROR, format=FORMAT)

credentials = pika.PlainCredentials(USER, PASS)

class RabbitMQWorker(object):

    '''
    This defines a worker that pulls messages from the queue and 
    executes the task. 

    This is the message consumer.
    '''

    def __init__(self): 

        '''
        Initialise a new connection to the queue.
        '''

        # Set up RabbitMQ connection
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host = HOST, 
                port = PORT, 
                credentials = credentials
            )
        )

        # Create the channel
        self.channel = self.connection.channel()

        # Declare the queue
        self.channel.queue_declare(queue='rpc_queue')

        logging.info(f'WORKER: new connection created {HOST}:{PORT}')



    
    def on_request(self, ch, method, props, body):
        '''
        This parses the body of messages from the queue. It then 
        calls the function which runs the values from the message
        as a query against the DB. Finally it inserts the results 
        into a queue.
        '''
        
        logging.info(f'WORKER: request recieved {props.correlation_id}')

        # Parse message body into dicts
        request = json.loads(body) 

        # Open a connection to the database
        db = get_db()

        # Query the database
        response = get_metadata(

            next(db), # Must call next() as db is a generator
            request.get('name'),
            request.get('db_type'),
            request.get('release'),
            request.get('offset'),
            request.get('limit'),

        )

        # Publish the results in the return queue
        ch.basic_publish(

            exchange = '',
            routing_key = props.reply_to,
            properties = pika.BasicProperties(
                correlation_id = props.correlation_id),
            body=json.dumps(response)

        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

        logging.info(f'WORKER: response sent {props.correlation_id}')
    
    def consume(self): 
        '''
        This starts the worker consuming messages.
        '''

        # Configure quality of service
        self.channel.basic_qos(
            prefetch_size = 0, 
            prefetch_count = 1
        )

        # Configure the queue
        self.channel.basic_consume(
            queue = 'rpc_queue', 
            on_message_callback = self.on_request
        )

        logging.info(f'WORKER: consuming...')
        
        # Start listening
        self.channel.start_consuming()



if __name__ == '__main__':

    worker = RabbitMQWorker()    
    worker.consume()




