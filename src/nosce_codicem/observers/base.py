class BaseObserver:
    """
    모든 Observer(variable, list 등)의 공통 인터페이스.
    '현재 상태를 가져오는 역할'
    """

    def capture(self, locals_dict):
        """
        현재 지역변수(locals_dict)에서
        필요한 값을 추출하여 반환한다.
        구체적인 로직은 각 Observer에서 구현한다.
        """
        raise NotImplementedError
