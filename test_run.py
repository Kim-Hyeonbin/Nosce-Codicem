from src.nosce_codicem.core.controller import controller
from src.nosce_codicem.observers.variable import VariableObserver
from src.nosce_codicem.handlers.loop import LoopHandler

# 1) 추적할 변수 이름
observer = VariableObserver(["x", "y"])

# 2) LoopHandler: 8줄~12줄만 관찰한다고 가정
handler = LoopHandler(line_start=8, line_end=12, observer=observer)

# 3) 컨트롤러에 핸들러 등록
controller.register_handler(handler)


def target_function():
    x = 0
    y = 10
    for i in range(3):  # ← (loop body는 대략 8~12 사이에 있다고 가정)
        x = x + 1
        y = y + 2
    return x + y


# 4) trace 시작
controller.start_trace()

target_function()

controller.stop_trace()
