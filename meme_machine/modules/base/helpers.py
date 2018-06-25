from modules.base.settings import (MENTION_ERROR_TOO_FEW,
                                   MENTION_ERROR_TOO_MANY,
                                   MENTION_ERROR_BOT_MENTIONED)


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


def first(predicate, l):
    """Returns the value that fulfils the predicate function

    :param predicate: The predicate to fulfil
    :type predicate: function val -> bool.
    """
    for item in l:
        if predicate(item):
            return item
    return None


def validate_num_of_mentions(mentions, num, user_only=True):
    """Validates that the number of mentions in `mentions` is `num`.

    :param mentions: The mentions in the message
    :type mentions: Discord message's mentions
    :param num: The number of mentions expected
    :type num: int.
    :returns: str|None -- None if the arugment is valid. A string with the
    error message otherwise.
    """
    if len(mentions) > num:
        return MENTION_ERROR_TOO_MANY
    elif len(mentions) < num:
        return MENTION_ERROR_TOO_FEW
    elif user_only and any(map(lambda x: x.bot, mentions)):
        return MENTION_ERROR_BOT_MENTIONED
    else:
        return None
