# sys.settrace의 속성을 정제하기 위한 클래스
# nosce_codicem/core/event.py
from dataclasses import dataclass


@dataclass  # 클래스를 구조체처럼 정의
class TraceEvent:
    """
    PHASE 0 최소 이벤트 구조체.
    - event_type: "call" / "line" / "return"
    - lineno: 현재 줄 번호
    - func_name: 함수 이름
    (filename, locals, timestamp 등은 이후 단계에서 추가)
    """

    event_type: str
    lineno: int
    func_name: str
    frame_locals: dict = None
