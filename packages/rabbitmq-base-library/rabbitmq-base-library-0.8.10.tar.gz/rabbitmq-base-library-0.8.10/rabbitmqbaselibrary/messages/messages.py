import json

import rabbitpy


class AmqpSenderConsumer(object):

    def __init__(self, conn_string: str):
        self.__amqp = rabbitpy.AMQP(rabbitpy.Connection(conn_string).channel())

    def publish_message(self, exchange: str, routing_key: str, message: dict) -> None:
        self.__amqp.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(message), mandatory=True)

    def receive_message(self, queue: str) -> dict:
        received: dict = {}
        for message in self.__amqp.basic_consume(queue=queue):
            message.ack()
            self.__amqp.basic_cancel()
            received = message.json()
            break
        return received


def build_conn_string(host: str, vhost: str, name: str, passwd: str) -> str:
    return 'amqps://{}:{}@{}/{}'.format(name, passwd, host, vhost)
