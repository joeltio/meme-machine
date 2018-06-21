from sqlalchemy.orm import sessionmaker

from database import create_engine
from modules.base.helpers import limit_command_arg
from modules.base.models import get_or_create_user
from modules.credits.models import get_or_create_credit


@limit_command_arg(2)
async def donate(client, message, receiver_tag, str_amount):
    # Validate incoming arguments
    try:
        if not str_amount.isdigit():
            error_message = ("Invalid argument type: amount given should be "
                             "an integer.")
            raise Exception(error_message)
        elif message.author.mention == receiver_tag:
            error_message = "Error: Cannot donate PP to yourself."
            raise Exception(error_message)
        elif len(message.mentions) < 1:
            error_message = "Error: No users were mentioned to receive the PP."
            raise Exception(error_message)
        elif len(message.mentions) > 1:
            error_message = ("Error: Too many users were mentioned to receive "
                             "the PP.")
            raise Exception(error_message)
        elif message.mentions[0].bot:
            error_message = "Error: A bot cannot receive PP."
            raise Exception(error_message)
    except Exception as e:
        await client.send_message(message.channel, e)
        return

    amount = int(str_amount)

    sender_discord = message.author
    receiver_discord = message.mentions[0]

    # Start a session
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Create both users if they do not already exist
    sender_user = get_or_create_user(session, sender_discord)
    receiver_user = get_or_create_user(session, receiver_discord)

    # 2. Create their credit records if they do not already exist
    sender_credit = get_or_create_credit(session, sender_user.id)
    receiver_credit = get_or_create_credit(session, receiver_user.id)

    # 3. Check if there is enough credits in the sending user
    if sender_credit.credits < amount:
        error_message = "Error: You do not have enough credits."
        await client.send_message(message.channel, error_message)

        session.commit()
        session.close()
        return

    # 4. Transfer the credits
    sender_credit.credits -= amount
    receiver_credit.credits += amount

    # 5. Commit and close the session
    session.commit()
    session.close()

    await client.send_message(message.channel,
                              f"Donated {amount}PP to {receiver_tag}")
