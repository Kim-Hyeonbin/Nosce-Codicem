from nosce_codicem.facade.trace_api import trace


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ---------------------------------------
# 테스트용 다중 리스트 추적
# ---------------------------------------
# arr  : 최초 입력 리스트
# left : 재귀에서 생성되는 왼쪽 조각
# right: 재귀에서 생성되는 오른쪽 조각
# merged: 병합 중 만들어지는 리스트

trace.list("arr", "left", "right", "merged").recursion("merge_sort")

arr = [
    57,
    12,
    89,
    43,
    7,
    66,
    31,
    24,
    95,
    18,
    72,
    4,
    53,
    28,
    61,
    39,
    83,
    10,
    47,
    92,
    6,
    34,
    77,
    15,
    58,
    21,
    84,
    9,
    69,
    304,
]
merge_sort(arr)
