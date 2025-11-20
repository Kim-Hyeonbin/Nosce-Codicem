from .base import BaseObserver


# 변수 추적하는 클래스
class VariableObserver(BaseObserver):

    def __init__(self, var_names):
        self.var_names = var_names
        self.mode = "variable"

    def capture(self, locals_dict):
        snapshot = {}

        for name in self.var_names:
            val = locals_dict.get(name)

            # 리스트/딕셔너리/셋/튜플 등 '컬렉션 자료형'은 변수로 취급하지 않음
            if isinstance(val, (list, tuple, dict, set)):
                snapshot[name] = None
            else:
                snapshot[name] = val

        return snapshot
