import requests
from pyramda import map, contains

from rabbitmqbaselibrary.common.handlers import handle_rest_response, handle_rest_response_with_body


def is_present(broker: dict, vhost: str, name: str) -> bool:
    return contains(name, get_queues(broker=broker, vhost=vhost))


# noinspection PyDeepBugsSwappedArgs
def get_queues(broker: dict, vhost: str) -> dict:
    url = 'https://{}/api/queues/{}'.format(broker['host'], vhost)
    response = requests.get(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
    return map(lambda i: i['name'], response.json())


def create_queue(broker: dict, vhost: str, name: str, queue: dict) -> None:
    url = 'https://{}/api/queues/{}/{}'.format(broker['host'], vhost, name)
    response = requests.put(url=url, auth=(broker['user'], broker['passwd']), json=queue)
    handle_rest_response_with_body(response=response, url=url, body=queue)


def delete_queue(broker: dict, vhost: str, name: str) -> None:
    url = 'https://{}/api/queues/{}/{}'.format(broker['host'], vhost, name)
    response = requests.delete(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
