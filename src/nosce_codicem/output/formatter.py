class BaseFormatter:
    """
    모든 Formatter의 기반 클래스.
    - 문자열이 아니라 JSON으로 직렬화 가능한 dict만 반환해야 함.
    - 렌더러(또는 viewer)가 UI와 스타일을 책임지므로
      formatter는 "데이터 정제"만 담당.
    """

    def format(self, event, snapshot, meta):
        """
        event : TraceEvent 객체 전체
        snapshot : observer.capture() 결과 (dict)
        meta : handler가 전달하는 부가 정보(ex. iteration, depth 등)
        """
        raise NotImplementedError("format() must be overridden.")


class LoopFormatter(BaseFormatter):
    """
    반복문(loop) 전용 formatter.
    handler에서 iteration 정보를 meta로 넘겨주면
    그걸 그대로 구조화해서 반환한다.
    """

    def format(self, event, snapshot, meta):
        return {
            "type": "loop",
            "lineno": event.lineno,
            "iteration": meta.get("iteration"),
            "variables": snapshot,
            "func_name": event.func_name,
        }


class RecursionFormatter(BaseFormatter):
    """
    재귀 호출 전용 formatter.
    - depth: 재귀 깊이
    - call_id: 이 호출의 ID (스택 기반으로 할당)
    - parent_id: 부모 호출의 ID
    """

    def format(self, event, snapshot, meta):
        return {
            "type": "recursion",
            "event_type": meta.get("event_type"),
            "lineno": event.lineno,
            "depth": meta.get("depth"),
            "variables": snapshot,
            "func_name": event.func_name,
            "call_id": meta.get("call_id"),
            "parent_id": meta.get("parent_id"),
            "mode": meta.get("mode"),
        }
