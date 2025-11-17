from .base import BaseObserver
import copy


class ListObserver(BaseObserver):
    def __init__(self, list_names):
        self.list_names = list_names

    def capture(self, locals_dict):
        snapshot = {}
        for name in self.list_names:
            val = locals_dict.get(name)
            if isinstance(val, list):
                snapshot[name] = copy.deepcopy(val)
            else:
                snapshot[name] = None
        return snapshot
