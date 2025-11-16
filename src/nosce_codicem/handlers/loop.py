from .base import BaseHandler
from ..output.formatter import Formatter


class LoopHandler(BaseHandler):
    """
    지정된 line 범위(line_start ~ line_end) 안에서
    observer.capture()로 가져온 값을 그대로 출력하는 단순 loop handler.
    """

    def __init__(self, line_start, line_end, observer, formatter=None, renderer=None):
        self.line_start = line_start
        self.line_end = line_end
        self.observer = observer
        self.renderer = renderer or print  # 기본 출력 방식
        self.formatter = formatter or Formatter()
        self.iteration = 0  # 루프 반복 횟수
        self._prev_lineno = None
        self._last_i = object()  # 어떤 값도 같지 않은 sentinel, 마지막 루프임을 확인

    def match_event(self, event):
        # 루프 내부 line 이벤트만 처리
        return (
            event.event_type == "line"
            and self.line_start <= event.lineno <= self.line_end
        )

    def handle(self, event):
        lineno = event.lineno

        # for 문 헤더 (iteration 시작) 감지
        if lineno == self.line_start:
            self.iteration += 1

        # 출력이 한 칸씩 밀리는 문제 해결
        # 1) 먼저, 직전 줄에 대한 정보를 출력
        if self._prev_lineno is not None:
            snapshot = self.observer.capture(self._prev_locals)
            if snapshot:
                formatted = self.formatter.format(
                    self._prev_lineno, snapshot, self.iteration
                )
                self.renderer(formatted)

        # 2) 그리고 지금 이벤트를 "다음에 출력할 직전 정보"로 저장
        self._prev_lineno = event.lineno
        self._prev_locals = event.frame_locals
