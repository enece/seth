import math


def fraction_from_decimal(decimal: float):
    decimal_rounded = round(decimal, 5)
    init_numerator = int(math.modf(decimal_rounded)[1])
    numerator = init_numerator
    denominator = 1

    while True:
        possible_answer = round(numerator/denominator, 5)
        if possible_answer == decimal_rounded:
            return str(numerator) + '/' + str(denominator)
        elif possible_answer > decimal_rounded:
            denominator += 1
            numerator = denominator * init_numerator
        else:
            numerator += 1
