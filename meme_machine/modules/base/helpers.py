import modules.base.settings as base_settings


def limit_command_arg(num_args):
    """Decorator to limit the number of arguments that can be given to a
    command. An error message will be sent when there is an incorrect number of
    arguments."""
    def decorator(f):
        async def wrapper(client, message, *args):
            if len(args) != num_args:
                error_message = base_settings.ARGUMENT_ERROR_WRONG_AMOUNT \
                    .format(expected=num_args, given=len(args))

                await client.send_message(message.channel, error_message)
            else:
                await f(client, message, *args)

        return wrapper
    return decorator


def collate_args(before_collate, after_collate=0):
    """Decorator to specify which part of the arguments to join. The argument
    that is made from joining multiple arguments is called the collate
    argument.

    The first `before_collate` arguments will be passed in. The arguments from
    `before_collate` onwards but before `after_collate` number of arguments
    will be combined.

    For example:
    ```
    @collate_args(2, 3)
    def f(client, message, a, b, c, d, e, f):
        pass

    # This is how arguments will be passed
    f(client, message,
      arg[0], arg[1],               # 2 arguments are passed first
      " ".join(arg[2:-3]),           # The arguments in between are joined
      arg[-3], arg[-2], arg[-1])    # 3 arguments at the back are passed
    ```

    :param before_collate: The number of arguments there should be before the
    collate argument
    :type before_collate: int.
    :param after_collate: The number of arguments there should be after the
    collate argument
    :type after_collate: int.
    :returns: decorator
    """
    def decorator(f):
        async def wrapper(client, message, *args):
            expected_num_args = before_collate + after_collate + 1
            if len(args) < expected_num_args:
                error_message = base_settings.ARGUMENT_ERROR_WRONG_AMOUNT \
                    .format(expected=">" + str(expected_num_args),
                            given=len(args))

                await client.send_message(message.channel, error_message)
            else:
                before_args = args[:before_collate]

                if after_collate == 0:
                    collate_arg = " ".join(args[before_collate:])
                    after_args = []
                else:
                    collate_arg = " ".join(args[before_collate:-after_collate])
                    after_args = args[-after_collate:]

                await f(client, message, *before_args,
                        collate_arg, *after_args)

        return wrapper
    return decorator


def validate_num_of_mentions(mentions, num, user_only=True):
    """Validates that the number of mentions in `mentions` is `num`.

    :param mentions: The mentions in the message
    :type mentions: Discord message's mentions
    :param num: The number of mentions expected
    :type num: int.
    :returns: str|None -- None if the argument is valid. A string with the
    error message otherwise.
    """
    if len(mentions) > num:
        return base_settings.MENTION_ERROR_TOO_MANY
    elif len(mentions) < num:
        return base_settings.MENTION_ERROR_TOO_FEW
    elif user_only and any(map(lambda x: x.bot, mentions)):
        return base_settings.MENTION_ERROR_BOT_MENTIONED
    else:
        return None


def validate_is_int(num, disallow_negative=False):
    """Validates that the number is an integer.

    :param num: The number to validate
    :type num: str.
    :param disallow_negative: Whether the number should not be negative
    :type disallow_negative: bool.
    :returns: str|None -- None if the argument is valid. A string with the
    error message otherwise.
    """
    # If the number >= 0
    if disallow_negative or num[0] != "-":
        if not num.isdigit():
            return base_settings.INT_ERROR_NOT_VALID
        return None

    # The number is negative
    if not num[1:].isdigit():
        return base_settings.INT_ERROR_NOT_VALID
    return None


def validate_is_range(start, end, allow_equals=True):
    """Validates that the start is smaller than the end. Assumes that the start
    and end are valid floats.

    :param start: The start of the range
    :type start: str.
    :param end: The end of the range
    :type end: str.
    :param allow_equals: Whether to allow the start to be equivalent to the end
    :type allow_equals: bool.
    :returns: str|None -- None if the argument is valid. A string with the
    error message otherwise.
    """
    if float(start) > float(end):
        return base_settings.RANGE_ERROR_START_AFTER_END

    if not allow_equals and float(start) == float(end):
        return base_settings.RANGE_ERROR_START_EQ_END

    return None


def validate_is_hex(val, digits):
    """Validates that the value is a hexadecimal with the specified number of
    digits and is represented in the format "0x0000".

    :param val: The value to validate
    :type val: str.
    :param digits: The number of digits the value should have
    :type digits: int.
    :returns: str|None -- None if the argument is valid. A string with the
    error message otherwise.
    """
    if digits <= 0:
        return None
    elif len(val) != (digits+2) or \
            val[:2] != "0x":
        return base_settings.HEX_ERROR_NOT_VALID.format(digits=digits)
    else:
        try:
            int(val, 16)
            return None
        except ValueError:
            return base_settings.HEX_ERROR_NOT_VALID.format(digits=digits)
