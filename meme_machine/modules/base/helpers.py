import modules.base.settings as base_settings


def limit_command_arg(num_args):
    """Decorator to limit the number of arguments that can be given to a
    command. An error message will be sent when there is an incorrect number of
    arguments."""
    def decorator(f):
        async def wrapper(client, message, *args):
            if len(args) != num_args:
                error_message = (
                    "Error: Incorrect number of arguments. Expected {}. "
                    "Given {}".format(num_args, len(args)))

                await client.send_message(message.channel, error_message)
            else:
                await f(client, message, *args)

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


def validate_is_int(num, only_positive=True):
    """Validates that the number is an integer.

    :param num: The number to validate
    :type num: str.
    :param only_positive: Whether the number should only be positive
    :type only_positive: bool.
    :returns: str|None -- None if the argument is valid. A string with the
    error message otherwise.
    """
    # If the number is positive
    if only_positive or num[0] != "-":
        if not num.isdigit():
            return base_settings.INT_ERROR_NOT_VALID
        return None

    # The number is negative
    if not num[1:].isdigit():
        return base_settings.INT_ERROR_NOT_VALID
    return None
