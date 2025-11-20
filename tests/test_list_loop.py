from nosce_codicem import trace


def test_list_loop():
    trace.list("arr", "brr").loop(13, 16)

    def list_test():
        arr = [1, 2, 3, 4, 5]
        brr = [10, 20, 30, 40, 50]

        i = 0

        while i < len(arr):  # 13
            arr[i] = arr[i] + brr[i]
            brr[i] = brr[i] // 2
            i += 1  # 16

        return arr, brr

    result = list_test()
    assert result == ([11, 22, 33, 44, 55], [5, 10, 15, 20, 25])
