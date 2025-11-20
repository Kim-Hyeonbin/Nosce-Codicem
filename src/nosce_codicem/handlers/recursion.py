from .base import BaseHandler
from ..output.formatter import RecursionFormatter
from ..output.renderer import Renderer


class RecursionHandler(BaseHandler):
    """
    재귀 호출 전용 핸들러.

    - target_func_name: 추적할 재귀 함수 이름
    - observer: VariableObserver / ListObserver 등
    - formatter: 기본값 RecursionFormatter
    - renderer: 기본값 Renderer (viewer.py 호출)
    """

    def __init__(self, target_func_name, observer, formatter=None, renderer=None):
        self.target_func_name = target_func_name
        self.observer = observer
        self.formatter = formatter or RecursionFormatter()
        self.renderer = renderer or Renderer()
        self.mode = observer.mode

        # 콜 트리용 스택
        self.call_stack = []  # 현재 활성화된 call_id 스택
        self.call_counter = 0  # 전역 고유 call_id

        # 기록 저장
        self.records = []

    # 어떤 이벤트를 받을지 결정
    def match_event(self, event):
        # 다른 함수는 무시
        if event.func_name != self.target_func_name:
            return False
        # 재귀 추적에 필요한 이벤트만
        return event.event_type in ("call", "line", "return")

    def _make_meta(self, event_type: str):
        """
        현재 call_stack 상태를 기반으로 meta 정보 생성.
        (call_id, parent_id, depth, event_type)
        """
        if not self.call_stack:
            # 비정상 상황 방지용
            return {
                "depth": 0,
                "call_id": None,
                "parent_id": None,
                "event_type": event_type,
                "mode": self.mode,
            }

        call_id = self.call_stack[-1]
        parent_id = self.call_stack[-2] if len(self.call_stack) >= 2 else None
        depth = len(self.call_stack)

        return {
            "depth": depth,
            "call_id": call_id,
            "parent_id": parent_id,
            "event_type": event_type,
            "mode": self.mode,
        }

    def handle(self, event):
        etype = event.event_type

        # call 이벤트: 새 호출 진입

        if etype == "call":
            # 새 call_id 발급 + 스택 push
            self.call_counter += 1
            call_id = self.call_counter
            parent_id = self.call_stack[-1] if self.call_stack else None
            self.call_stack.append(call_id)

            # 이 시점에서의 depth는 push 이후 기준
            depth = len(self.call_stack)

            snapshot = self.observer.capture(event.frame_locals)
            if snapshot:
                meta = {
                    "depth": depth,
                    "call_id": call_id,
                    "parent_id": parent_id,
                    "event_type": "call",
                    "mode": self.mode,
                }
                formatted = self.formatter.format(
                    event=event,
                    snapshot=snapshot,
                    meta=meta,
                )
                self.records.append(formatted)

            return

        # return 이벤트: 호출 종료

        if etype == "return":
            if not self.call_stack:
                # 이상한 상황이면 그냥 무시
                return

            # pop 하기 전에 현재 call_id/parent_id/깊이로 메타 구성
            meta = self._make_meta("return")

            snapshot = self.observer.capture(event.frame_locals)
            if snapshot:
                formatted = self.formatter.format(
                    event=event,
                    snapshot=snapshot,
                    meta=meta,
                )
                self.records.append(formatted)

            # 실제로 콜 스택에서 제거
            self.call_stack.pop()
            return

        # line 이벤트: 현재 호출 내부 상태 기록

        if etype == "line":
            if not self.call_stack:
                # 우리가 관리하는 콜 스택 밖에서 날아온 라인이면 무시
                return

            meta = self._make_meta("line")
            snapshot = self.observer.capture(event.frame_locals)
            if snapshot:
                formatted = self.formatter.format(
                    event=event,
                    snapshot=snapshot,
                    meta=meta,
                )
                self.records.append(formatted)

            return

    def finalize(self):
        """
        trace 종료 시 controller가 호출.
        기록이 있으면 viewer를 recursion 모드로 실행.
        """
        if self.records:
            self.renderer(self.records, dtype="recursion")
