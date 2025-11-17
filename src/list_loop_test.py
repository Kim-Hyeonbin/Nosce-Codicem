from nosce_codicem.facade.trace_api import trace

# 리스트 두 개 추적, 루프 시작은 line 13
trace.list("arr", "brr").loop(13, 16)


def list_test():
    arr = [1, 2, 3, 4, 5]
    brr = [10, 20, 30, 40, 50]

    i = 0

    while i < len(arr):  # line 13
        arr[i] = arr[i] + brr[i]
        brr[i] = brr[i] // 2
        i += 1  # 16

    return arr, brr


print(list_test())
