from modules.base.helpers import limit_command_arg


@limit_command_arg(2)
async def donate(client, message, receiver_tag, amount):
    # Validate incoming arguments
    try:
        if not amount.isdigit():
            error_message = ("Invalid argument type: amount given should be "
                             "an integer")
            raise Exception(error_message)
        elif message.author.mention == receiver_tag:
            error_message = "Error: Cannot donate PP to yourself"
            raise Exception(error_message)
        elif len(message.mentions) < 1:
            error_message = "Error: No users were mentioned to receive the PP"
            raise Exception(error_message)
        elif len(message.mentions) > 1:
            error_message = ("Error: Too many users were mentioned to receive "
                             "the PP")
            raise Exception(error_message)
        elif message.mentions[0].bot:
            error_message = "Error: A bot cannot receive PP"
            raise Exception(error_message)
    except Exception as e:
        await client.send_message(message.channel, e)
        return

    await client.send_message(message.channel,
                              f"Donated {amount}PP to {receiver_tag}")
