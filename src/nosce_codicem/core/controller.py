import sys
from .event import TraceEvent


class TraceController:
    """
    PHASE 0용 최소 TraceController.
    - sys.settrace 등록/해제
    - frame, event를 받아서 TraceEvent로 변환
    - 일단은 print만 하고, dispatch_event는 빈 껍데기
    """

    def __init__(self):
        # 현재 trace 중인지 여부를 나타내는 플래그 변수
        self._tracing = False

    # settrace에 직접 넘길 콜백
    def _trace_func(self, frame, event, arg):
        # PHASE 0에서는 call/line/return만 신경 씀
        if event not in ("call", "line", "return"):
            # exception 등의 상황에서도 추적은 유지
            return self._trace_func

        # frame을 통해 코드 객체 생성
        code = frame.f_code

        # 이벤트 추적 객체 생성
        evt = TraceEvent(
            event_type=event,  # 이벤트 타입 부여
            lineno=frame.f_lineno,  # 현재 프레임이 실행 중인 줄 번호
            func_name=code.co_name,  # 코드 객체의 이름 (함수 이름)
        )

        # 최소 기능: 그냥 찍어보기
        print(f"[TRACE] {evt.event_type:6} {evt.func_name} @ line {evt.lineno}")

        # 이후 PHASE 1에서 핸들러에게 넘기도록 확장
        self.dispatch_event(evt)

        # 자기 자신을 리턴해야 전체 실행 동안 추적 유지
        return self._trace_func

    def start_trace(self):
        """
        전역 trace 시작
        """
        if self._tracing:
            # 이미 tracing 중이면 다시 걸지 않음
            return

        self._tracing = True
        sys.settrace(self._trace_func)

    def stop_trace(self):
        """
        전역 trace 중단
        """
        if not self._tracing:
            return

        self._tracing = False
        sys.settrace(None)

    def dispatch_event(self, event: TraceEvent):
        """
        PHASE 0에서는 아무것도 하지 않는 껍데기.
        이후 PHASE 1에서 handler들에게 전달하는 로직 추가 예정.
        """
        pass


# 간단한 싱글톤 스타일로 써먹기 좋게 하나 임시로 만들어 둠
controller = TraceController()
