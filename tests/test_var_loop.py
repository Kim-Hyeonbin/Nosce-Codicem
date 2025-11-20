from nosce_codicem import trace

trace.variable("i", "current", "min_val", "max_val", "count", "bool").loop(16, 27)


def variable_test():
    nums = [7, 3, 9, 1, 8, 2]

    i = 0
    current = 0
    min_val = 10000
    max_val = -(10**9)
    count = 0
    bool = False

    while i < len(nums):  # line 16
        current = nums[i]

        if current < min_val:
            min_val = current

        if current > max_val:
            max_val = current

        bool = not bool
        count += 1
        i += 1

    return min_val, max_val, count


print(variable_test())
