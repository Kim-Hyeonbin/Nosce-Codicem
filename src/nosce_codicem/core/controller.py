import sys
import atexit
from .event import TraceEvent


class TraceController:
    """
    - sys.settrace 등록/해제
    - frame, event를 받아서 TraceEvent로 변환
    """

    def __init__(self):
        self._tracing = False
        self._handlers = []

        # 프로그램이 끝날 때 자동으로 정리
        atexit.register(self._on_exit)

    def _on_exit(self):
        """
        인터프리터 종료 직전에 자동 호출됨.
        tracing이 활성화되어 있다면 stop_trace() 호출해
        모든 handler의 finalize()가 실행되도록 한다.
        """
        if self._tracing:
            self.stop_trace()

    def _trace_func(self, frame, event, arg):
        # 내부 trace 함수들은 무시
        if frame.f_code.co_name in (
            "start_trace",
            "stop_trace",
            "_trace_func",
            "dispatch_event",
        ):
            return self._trace_func

        filename = frame.f_code.co_filename.replace("\\", "/")

        # 너무 넓은 제외 조건 → 세분화
        if "/nosce_codicem/handlers/" in filename:
            return self._trace_func
        if "/nosce_codicem/observers/" in filename:
            return self._trace_func
        if "/nosce_codicem/output/" in filename:
            return self._trace_func

        code = frame.f_code
        try:
            evt = TraceEvent(
                event_type=event,
                lineno=frame.f_lineno,
                func_name=code.co_name,
                frame_locals=frame.f_locals,
            )
        except Exception:
            return self._trace_func

        self.dispatch_event(evt)
        return self._trace_func

    def register_handler(self, handler):
        self._handlers.append(handler)

    def start_trace(self):
        if self._tracing:
            return
        self._tracing = True
        sys.settrace(self._trace_func)

    def stop_trace(self):
        """
        전역 trace 중단 + 핸들러 finalize 호출
        """
        if not self._tracing:
            return

        self._tracing = False
        sys.settrace(None)

        # ★ 여기서 모든 handler의 finalize()를 한 번씩 호출
        for h in self._handlers:
            finalize = getattr(h, "finalize", None)
            if callable(finalize):
                try:
                    finalize()
                except Exception as e:
                    print(
                        f"[TraceController] finalize() error in {h}: {e}",
                        file=sys.stderr,
                    )

    def dispatch_event(self, event: TraceEvent):
        for h in self._handlers:
            if h.match_event(event):
                h.handle(event)


controller = TraceController()
