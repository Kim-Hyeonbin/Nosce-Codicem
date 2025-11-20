from nosce_codicem.facade.trace_api import trace


def partition_sum(arr):
    size = len(arr)
    if size <= 1:
        return sum(arr)

    half = size // 2
    left = partition_sum(arr[:half])
    right = partition_sum(arr[half:])
    total = left + right
    return total


trace.variable("arr", "size", "half", "left", "right", "total").recursion(
    "partition_sum"
)

print(partition_sum([5, 2, 7, 1, 9]))
