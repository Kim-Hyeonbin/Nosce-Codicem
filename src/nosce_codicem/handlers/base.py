class BaseHandler:
    """
    모든 Handler(loop, recursive, condition 등)의 공통 인터페이스.

    Handler는 두 가지 역할을 가진다:
    1) match_event(event): 지금 이벤트에 반응할지 결정
    2) handle(event): 반응할 경우 observer 등을 사용해 처리
    """

    def match_event(self, event):
        """
        이 이벤트를 처리할지 여부를 결정.
        True 또는 False를 반환해야 함.
        """
        raise NotImplementedError

    def handle(self, event):
        """
        이벤트가 이 Handler의 조건에 맞았을 때 실행되는 로직.
        (예: observer.capture → diff → 출력)
        """
        raise NotImplementedError
