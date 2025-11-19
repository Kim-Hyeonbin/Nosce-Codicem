from .base import BaseHandler
from ..output.formatter import RecursionFormatter
from ..output.renderer import Renderer


class RecursionHandler(BaseHandler):
    def __init__(self, target_func_name, observer, formatter=None, renderer=None):
        self.target_func_name = target_func_name
        self.observer = observer
        self.formatter = formatter or RecursionFormatter()
        self.renderer = renderer or Renderer()

        self.depth = 0
        self.records = []

        # 마지막 버퍼용
        self._prev_event = None
        self._prev_locals = None

    def match_event(self, event):
        return event.func_name == self.target_func_name

    def handle(self, event):
        etype = event.event_type

        # 버퍼 flush (이전 이벤트 기록)
        if self._prev_event is not None:
            snapshot = self.observer.capture(self._prev_locals)
            if snapshot:
                formatted = self.formatter.format(
                    event=self._prev_event,
                    snapshot=snapshot,
                    meta={"depth": self.depth},
                )
                self.records.append(formatted)

        # 깊이 변경
        if etype == "call":
            self.depth += 1

        elif etype == "return":
            # return에서는 locals 상태가 이미 끝난 프레임이므로 기록 X
            self.depth -= 1

        # 이번 이벤트를 다음에 기록할 버퍼로 저장
        self._prev_event = event
        self._prev_locals = event.frame_locals

    def finalize(self):
        # 마지막 버퍼 flush
        if self._prev_event is not None:
            snapshot = self.observer.capture(self._prev_locals)
            if snapshot:
                formatted = self.formatter.format(
                    event=self._prev_event,
                    snapshot=snapshot,
                    meta={"depth": self.depth},
                )
                self.records.append(formatted)

        # viewer 실행
        if self.records:
            self.renderer(self.records, dtype="recursion")
