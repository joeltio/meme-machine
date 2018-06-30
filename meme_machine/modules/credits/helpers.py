import modules.base.helpers as base_helpers

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
    if base_helpers.validate_is_int(arg, True) is not None:
        return CREDIT_ERROR_INVALID_AMOUNT_TYPE
    else:
        return None


def validate_credit_range(start, end):
    """Validates that the starting range is smaller than the ending range.
    Assumes that the start and end of the range are valid floats.

    :param start: The start of the credit range
    :type start: str.
    :param end: The end of the credit range
    :type start: str.
    :returns: str|None -- None if the argument is valid. A string with the
    error message otherwise.
    """
    if base_helpers.validate_is_range(start, end, False) is not None:
        return CREDIT_ERROR_REVERSED_RANGE
    else:
        return None
