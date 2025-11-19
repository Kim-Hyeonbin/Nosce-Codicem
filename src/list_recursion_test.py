from nosce_codicem.facade.trace_api import trace


def sum_slice(arr):
    if not arr:
        return 0
    first = arr[0]
    rest = sum_slice(arr[1:])
    return first + rest


# 리스트 추적 모드로
trace.list("arr").recursion("sum_slice")

print("result =", sum_slice([1, 3, 5, 7]))
