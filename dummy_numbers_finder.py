"""
Bokijonov Mukhsinjon
52336
Task 2
"""


def dummy_numbers(an):
    if an == 0:
        yield 0
    elif an == 1:
        yield 0
        yield 1
    else:
        an_2, an_1 = None, None
        for an_0 in dummy_numbers(an - 1):
            an_2, an_1 = an_1, an_0
            yield an_0
        yield (an_2 + 1) * an_1


# Print the result
for num in dummy_numbers(10):
    print(num)
