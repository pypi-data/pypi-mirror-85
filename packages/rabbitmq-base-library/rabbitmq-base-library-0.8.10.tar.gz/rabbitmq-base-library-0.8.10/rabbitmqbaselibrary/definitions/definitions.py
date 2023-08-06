# noinspection PyDeepBugsSwappedArgs
import requests

from rabbitmqbaselibrary.common.handlers import handle_rest_response, handle_rest_response_with_body


# noinspection PyDeepBugsSwappedArgs
def get_definitions(broker: dict, vhost: str) -> dict:
    url = 'https://{}/api/definitions/{}'.format(broker['host'], vhost)
    response = requests.get(url=url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response, url)
    return response.json()


# noinspection PyDeepBugsSwappedArgs
def load_definitions(broker: dict, vhost: str, definitions: dict) -> None:
    url = 'https://{}/api/definitions/{}'.format(broker['host'], vhost)
    response = requests.post(url=url, auth=(broker['user'], broker['passwd']), json=definitions)
    handle_rest_response_with_body(response, url, definitions)
