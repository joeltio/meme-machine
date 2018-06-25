from modules.credits.settings import CREDIT_ERROR_INVALID_AMOUNT_TYPE


def validate_credit_arg(arg, only_positive=True):
    """Validates credit arguments for commands.

    :param arg: The value to validate. It is assumed that the string not empty
    :type arg: str.
    :param only_positive: Whether to allow negative values for the argument
    :type only_positive: bool.
    :returns: str|None -- None if the arugment is valid. A string with the
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
