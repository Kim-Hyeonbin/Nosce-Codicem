from .base import BaseHandler


class LoopHandler(BaseHandler):
    """
    특정 line 범위 (루프 본문) 안에서만 Observer를 실행하는 Handler.
    - line_start <= lineno <= line_end 일 때만 작동한다.
    - observer.capture()로 상태를 스냅샷
    - observer.diff()로 변화 계산
    """

    def __init__(self, line_start, line_end, observer, renderer=None):
        self.line_start = line_start
        self.line_end = line_end
        self.observer = observer
        self.renderer = renderer or print  # 기본은 print
        self.previous = None  # 이전 스냅샷을 저장할 속성

    def match_event(self, event):
        # 루프 내부의 'line' 이벤트일 때 작동
        if event.event_type != "line":
            return False

        # event.lineno이 지정된 범위일 때 True
        return self.line_start <= event.lineno <= self.line_end

    def handle(self, event):
        # 매 줄마다 snapshot -> diff -> 출력

        # locals 캡쳐
        frame_locals = event.frame_locals

        # 현재의 snapshot 생성
        snapshot = self.observer.capture(frame_locals)

        # diff 계산
        diff = self.observer.diff(self.previous, snapshot)

        # 변화가 있다면 출력
        if diff:
            self.renderer(f"[line {event.lineno}] {diff}")

        # 상태 업데이트
        self.previous = snapshot
