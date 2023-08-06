import json
import uuid
from datetime import datetime
from typing import List, Dict


class Report(object):
    __buffer: List[Dict] = []
    __context: dict = {}

    def set_context(self, context: dict) -> None:
        self.__context = context

    def append_event(self, name: str, record: dict) -> None:
        record.update({'context': self.__context})
        record.update({
            'id': str(uuid.uuid4()),
            'name': name,
            'timestamp': datetime.now().isoformat()
        })
        self.__buffer.append(record)

    def report(self) -> str:
        return json.dumps(self.__buffer, indent=4)
