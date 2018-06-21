from modules.base.actions import limit_command_arg


@limit_command_arg(2)
async def donate(client, message, *args):
    raise NotImplementedError()
