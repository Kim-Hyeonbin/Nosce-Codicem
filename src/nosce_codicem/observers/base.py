class BaseObserver:
    """
    모든 Observer(variable, list 등)의 공통 인터페이스.
    - capture(obj): 현재 상태를 스냅샷으로 저장
    - diff(old, new): 두 스냅샷의 차이를 계산
    """

    def capture(self, locals_dict):
        """
        현재 상태를 스냅샷으로 만들어 반환.
        각 Observer가 어떤 데이터를 캡처할지 결정함.
        예: VariableObserver → 특정 변수만 뽑아오기
        """
        raise NotImplementedError

    def diff(self, old, new):
        """
        두 스냅샷(old, new)의 차이를 계산.
        변화가 없으면 None, 변화가 있으면 변화 내용을 dict 등으로 반환.
        """
        raise NotImplementedError
