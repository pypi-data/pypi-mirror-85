from typing import List


def factorize(number: int) -> List[int]:
    """
    Factorize the given number.

    Parameters
    ----------
    number : int

    Returns
    -------
    factors : List[int]

    Examples
    --------
    >>> factorize(14)
    [2, 7]
    >>> factorize(-14)
    [-1, 2, 7]
    """
    factors = []
    if not isinstance(number, int):
        raise ValueError(f"integer expected, got {type(number)}")
    if number == 0:
        raise ValueError("0 cannot be factorized.")
    if number < 0:
        number *= -1
        factors.append(-1)
    if number == 1:
        if len(factors) == 0:
            factors.append(1)
        return factors
    for factor in range(2, number + 1):
        while number % factor == 0:
            factors.append(factor)
            number = int(number / factor)
        if number == 1:
            break
    return factors


if __name__ == "__main__":
    import doctest

    doctest.testmod()
