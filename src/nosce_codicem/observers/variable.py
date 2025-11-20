from .base import BaseObserver


# 변수 추적하는 클래스
class VariableObserver(BaseObserver):

    def __init__(self, var_names):
        self.var_names = var_names
        self.mode = "variable"

    def capture(self, locals_dict):
        return {name: locals_dict.get(name) for name in self.var_names}
