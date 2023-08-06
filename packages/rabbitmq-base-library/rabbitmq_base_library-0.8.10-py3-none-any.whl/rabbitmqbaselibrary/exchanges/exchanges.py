import requests
from pyramda import map, contains

from rabbitmqbaselibrary.common.handlers import handle_rest_response, handle_rest_response_with_body


def is_present(broker: dict, vhost: str, name: str) -> bool:
    return contains(name, get_exchanges(broker=broker, vhost=vhost))


# noinspection PyDeepBugsSwappedArgs
def get_exchanges(broker: dict, vhost: str) -> dict:
    url = 'https://{}/api/exchanges/{}'.format(broker['host'], vhost)
    response = requests.get(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
    return map(lambda i: i['name'], response.json())


def create_exchange(broker: dict, vhost: str, name: str, exchange: dict) -> None:
    url = 'https://{}/api/exchanges/{}/{}'.format(broker['host'], vhost, name)
    response = requests.put(url=url, auth=(broker['user'], broker['passwd']), json=exchange)
    handle_rest_response_with_body(response=response, url=url, body=exchange)


def delete_exchange(broker: dict, vhost: str, name: str) -> None:
    url = 'https://{}/api/exchanges/{}/{}'.format(broker['host'], vhost, name)
    response = requests.delete(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
