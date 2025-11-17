from .base import BaseHandler
from ..output.formatter import LoopFormatter
from ..output.renderer import Renderer
import sys


class LoopHandler(BaseHandler):
    """
    지정된 line 범위(line_start ~ line_end) 안에서
    observer.capture()로 가져온 값을 records에 저장하고,
    trace 종료 시 finalize()에서만 viewer를 실행하는 handler.
    """

    def __init__(self, line_start, line_end, observer, formatter=None, renderer=None):
        self.line_start = line_start
        self.line_end = line_end
        self.observer = observer
        self.formatter = formatter or LoopFormatter()
        self.renderer = renderer or Renderer()

        self.iteration = 0
        self._prev_lineno = None
        self._prev_locals = None
        self._prev_event = None

        self.records = []  # ← 모든 스냅샷 누적

    def match_event(self, event):
        result = (
            event.event_type == "line"
            and self.line_start <= event.lineno <= self.line_end
        )
        return result

    def handle(self, event):
        lineno = event.lineno

        # 1) 먼저, 직전 이벤트를 현재 iteration 값으로 기록
        if self._prev_lineno is not None:
            snapshot = self.observer.capture(self._prev_locals)
            if snapshot:
                formatted = self.formatter.format(
                    event=self._prev_event,
                    snapshot=snapshot,
                    meta={"iteration": self.iteration},
                )
                self.records.append(formatted)

        # 2) 그 다음, 이번 이벤트가 루프 시작 줄이면 그때 iteration 증가
        if lineno == self.line_start:
            self.iteration += 1

        # 3) 현재 이벤트를 다음 턴에 찍기 위해 버퍼에 저장
        self._prev_lineno = lineno
        self._prev_locals = event.frame_locals
        self._prev_event = event

    def finalize(self):
        """
        trace 종료 시 controller가 호출해주는 메서드.
        이때 단 한 번만 viewer를 실행한다.
        """
        # 마지막 버퍼도 flush
        if self._prev_event is not None:
            snapshot = self.observer.capture(self._prev_locals)
            if snapshot:
                formatted = self.formatter.format(
                    event=self._prev_event,
                    snapshot=snapshot,
                    meta={"iteration": self.iteration},
                )
                self.records.append(formatted)

        # 최종적으로 renderer를 딱 1번 호출
        if self.records:
            self.renderer(self.records, dtype="loop")
