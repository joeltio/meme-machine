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
