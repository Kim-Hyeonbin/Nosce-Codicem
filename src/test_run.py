from nosce_codicem.facade.trace_api import trace

trace.variable("i", "x", "y").loop(11, 18)


def sample_function():
    i = 0
    x = 5
    y = 1

    while i < 4:  # line 14
        x = x - i  # line 15
        y = y * 2  # line 16

        if x < 0:  # line 18
            break  # line 19

        i = i + 1  # line 20

    return x + y


sample_function()
