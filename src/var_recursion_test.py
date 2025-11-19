from nosce_codicem.facade.trace_api import trace


def fact(n):
    x = n  # 지역변수 1
    if n <= 1:
        return 1

    y = fact(n - 1)  # 지역변수 2
    z = x * y  # 지역변수 3
    return z


# 재귀문 변수 추적 시작
trace.variable("n", "x", "y", "z").recursion("fact")

print("result =", fact(4))
