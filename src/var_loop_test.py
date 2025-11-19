from nosce_codicem.facade.trace_api import trace

# 변수 네 개 이상 추적, 루프 시작은 line 10
trace.variable("i", "current", "min_val", "max_val", "count", "불리안").loop(17, 30)


def variable_test():
    nums = [7, 3, 9, 1, 8, 2]

    i = 0
    current = 0
    min_val = 10000
    max_val = -(10**9)
    count = 0
    불리안 = False

    while i < len(nums):  # line 16
        current = nums[i]

        if current < min_val:
            min_val = current

        if current > max_val:
            max_val = current

        불리안 = not 불리안

        count += 1
        i += 1

    return min_val, max_val, count


print(variable_test())
