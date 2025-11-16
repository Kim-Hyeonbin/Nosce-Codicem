# nosce_codicem/facade/trace_api.py

from ..core.controller import controller
from ..handlers.loop import LoopHandler
from ..observers.variable import VariableObserver


class TraceBuilder:
    def __init__(self):
        self._var_names = None

    def variable(self, *names):
        self._var_names = names
        return self

    def loop(self, line_start, line_end):
        # 1) Observer 생성
        observer = VariableObserver(self._var_names)

        # 2) Handler 생성
        handler = LoopHandler(line_start, line_end, observer)

        # 3) Controller에 등록
        controller.register_handler(handler)

        # 4) 자동 trace 시작
        controller.start_trace()

        return self


# 사용자가 import해서 쓸 단일 인터페이스
trace = TraceBuilder()
# trace 함수는 코드 맨 위에서 호출되어야 함
