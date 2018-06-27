from modules.credits.settings import (CREDIT_ERROR_INVALID_AMOUNT_TYPE,
                                      CREDIT_ERROR_REVERSED_RANGE)


def validate_credit_arg(arg, only_positive=True):
    """Validates credit arguments for commands.

    :param arg: The value to validate. It is assumed that the string not empty
    :type arg: str.
    :param only_positive: Whether to allow negative values for the argument
    :type only_positive: bool.
    :returns: str|None -- None if the argument is valid. A string with the
    error message otherwise.
    """
    # If the number is positive
    if only_positive or arg[0] != "-":
        if not arg.isdigit():
            return CREDIT_ERROR_INVALID_AMOUNT_TYPE
        return None

    # The number is negativ
    if not arg[1:].isdigit():
        return CREDIT_ERROR_INVALID_AMOUNT_TYPE
    return None


def validate_credit_range(start, end):
    """Validates that the starting range is smaller than the ending range.

    :param start: The start of the credit range
    :type start: int.
    :param end: The end of the credit range
    :type start: int.
    :returns: str|None -- None if the argument is valid. A string with the
    error message otherwise.
    """
    if start >= end:
        return CREDIT_ERROR_REVERSED_RANGE
    else:
        return None
