def calculate(tup) -> (float, float):
    (a, b) = tup
    mean = (a + b) / 2

    diff_a = a - mean
    new_a = mean - (diff_a / 2)

    diff_b = b - mean
    new_b = mean - (diff_b / 2)

    return new_a, new_b


print(calculate(calculate(calculate((1.0, 0.0)))))
