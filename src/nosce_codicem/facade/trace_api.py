from ..core.controller import controller
from ..handlers.loop import LoopHandler
from ..observers.variable import VariableObserver
from ..observers.list import ListObserver
from ..output.formatter import LoopFormatter
from ..output.renderer import Renderer


class TraceBuilder:
    def __init__(self):
        self._var_names = None
        self._list_names = None

    # 추적할 변수를 등록
    def variable(self, *names):
        self._var_names = names
        self._list_names = None  # 변수와 리스트 동시 추적 금지
        return self

    # 추적할 리스트를 등록
    def list(self, *names):
        self._list_names = names
        self._var_names = None  # 변수와 리스트 동시 추적 금지
        return self

    def loop(self, line_start, line_end):
        # 1) Observer 생성
        if self._var_names:
            observer = VariableObserver(self._var_names)
        elif self._list_names:
            observer = ListObserver(self._list_names)
        else:
            raise ValueError(
                "TraceBuilder: variable() 또는 list() 중 하나는 반드시 호출해야 합니다."
            )

        # 2) Handler 생성
        handler = LoopHandler(
            line_start,
            line_end,
            observer,
            formatter=LoopFormatter(),
            renderer=Renderer(),
        )

        # 3) Controller에 등록
        controller.register_handler(handler)

        # 4) 자동 trace 시작
        controller.start_trace()

        return self


# 사용자가 import해서 쓸 단일 인터페이스
trace = TraceBuilder()

# trace 함수는 코드 맨 위에서 호출되어야 함
