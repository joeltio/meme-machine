from modules.base.helpers import limit_command_arg


@limit_command_arg(2)
async def donate(client, message, *args):
    raise NotImplementedError()
    receiver, amount = args
    await client.send_message(message.channel,
                              f"Donated {amount}PP to {receiver}")
