# main.py
from nosce_codicem.facade.trace_api import trace

trace.variable("i", "x", "y", "z").loop(11, 14)


def sample_function():
    x = 0
    y = 10

    for i in range(3):
        x = x + 1
        y = y + i
        z = x + y

    return x + y


sample_function()

# 🔥 원하는 API 한 줄
# sample_function 안의 for 루프가 10~20줄이라고 가정한 예시
