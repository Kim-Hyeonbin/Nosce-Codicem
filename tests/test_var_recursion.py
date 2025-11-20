from nosce_codicem import trace


def fib(n):
    if n <= 1:
        return n

    # 추적용 임시 변수 두 개 추가
    a = fib(n - 1)
    b = fib(n - 2)

    result = a + b
    return result


# ---- 추적 ----
trace.variable("n", "a", "b", "result").recursion("fib")

fib(5)
