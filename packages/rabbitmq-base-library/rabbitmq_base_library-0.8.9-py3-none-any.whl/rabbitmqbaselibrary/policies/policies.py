import requests
from pyramda import map, contains

from rabbitmqbaselibrary.common.handlers import handle_rest_response, handle_rest_response_with_body


def is_present(broker: dict, vhost: str, name: str) -> bool:
    return contains(name, get_policies(broker=broker, vhost=vhost))


# noinspection PyDeepBugsSwappedArgs
def get_policies(broker: dict, vhost: str) -> dict:
    url = 'https://{}/api/policies/{}'.format(broker['host'], vhost)
    response = requests.get(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
    return map(lambda i: i['name'], response.json())


# noinspection PyDeepBugsSwappedArgs
def create_policy(broker: dict, vhost: str, name: str, policy: dict) -> None:
    url = 'https://{}/api/policies/{}/{}'.format(broker['host'], vhost, name)
    response = requests.put(url=url, auth=(broker['user'], broker['passwd']), json=policy)
    handle_rest_response_with_body(response=response, body=policy, url=url)


def delete_policy(broker: dict, vhost: str, name: str) -> None:
    url = 'https://{}/api/policies/{}/{}'.format(broker['host'], vhost, name)
    response = requests.delete(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
