from .base import BaseObserver


class VariableObserver(BaseObserver):
    """
    특정 변수들의 값을 추적하는 Observer.
    - var_names 리스트에 지정된 변수만 관찰한다.
    - capture(locals_dict) → {var: value}
    - diff(old, new) → 변화가 있으면 {var: (old, new)} 반환
                      변화 없으면 None
    """

    def __init__(self, var_name):
        # 추적할 변수 이름(혹은 이름 목록)
        self.var_name = var_name
        # 직전 스냅샷 저장용 변수
        self.previous = None

    def capture(self, locals_dict):
        # locals_dict에서 var_names에 해당하는 값만 뽑아 스냅샷 반환
        snapshot = {}
        for name in self.var_name:
            snapshot[name] = locals_dict.get(name)
        return snapshot

    def diff(self, old, new):
        # 두 스냅샷을 비교, 변경된 변수만 반환, 변화 없으면 None 리턴
        changes = {}

        for key in new:
            # 첫 번째 호출 상황
            if old is None:
                changes[key] = (None, new[key])
                continue

            # 변화가 있다면 (이전, 현재)의 튜플 형태로 저장
            if old.get(key) != new.get(key):
                changes[key] = (old.get(key), new.get(key))

        if changes:
            return changes

        return None
