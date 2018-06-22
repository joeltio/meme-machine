from sqlalchemy.orm import sessionmaker

from database import create_engine
from modules.base.helpers import limit_command_arg
from modules.base.models import get_or_create_user
from modules.credits.models import get_or_create_credit
from modules.credits.settings import *


@limit_command_arg(2)
async def donate(client, message, receiver_tag, str_amount):
    # Validate incoming arguments
    try:
        if not str_amount.isdigit():
            raise Exception(DONATE_ERROR_INVALID_AMOUNT_TYPE)
        elif int(str_amount) <= 0:
            raise Exception(DONATE_ERROR_AMOUNT_NOT_POSITIVE)
        elif message.author.mention == receiver_tag:
            raise Exception(DONATE_ERROR_SELF_DONATE)
        elif len(message.mentions) < 1:
            raise Exception(DONATE_ERROR_NO_USER_MENTIONED)
        elif len(message.mentions) > 1:
            raise Exception(DONATE_ERROR_TOO_MANY_USERS_MENTIONED)
        elif message.mentions[0].bot:
            raise Exception(DONATE_ERROR_BOT_MENTIONED)
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
        await client.send_message(
            message.channel, DONATE_ERROR_INSUFFICIENT_CREDITS)

        session.commit()
        session.close()
        return

    # 4. Transfer the credits
    sender_credit.credits -= amount
    receiver_credit.credits += amount

    # 5. Commit and close the session
    session.commit()
    session.close()

    success_message = DONATE_SUCCESS.format(
        amount=amount, receiver=receiver_tag)
    await client.send_message(message.channel, success_message)


@limit_command_arg(2)
async def admin_add(client, message, receiver_tag, str_amount):
    # Validate incoming arguments
    try:
        if not str_amount.isdigit():
            raise Exception(ADMIN_ADD_ERROR_INVALID_AMOUNT_TYPE)
        elif len(message.mentions) < 1:
            raise Exception(ADMIN_ADD_ERROR_NO_USER_MENTIONED)
        elif len(message.mentions) > 1:
            raise Exception(ADMIN_ADD_ERROR_TOO_MANY_USERS_MENTIONED)
        elif message.mentions[0].bot:
            raise Exception(ADMIN_ADD_ERROR_BOT_MENTIONED)
    except Exception as e:
        await client.send_message(message.channel, e)
        return

    amount = int(str_amount)
    receiver_discord = message.mentions[0]

    # Start a session
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    receiver_user = get_or_create_user(session, receiver_discord)
    receiver_credit = get_or_create_credit(session, receiver_user.id)
    receiver_credit.credits += amount

    session.commit()
    session.close()

    success_message = ADMIN_ADD_SUCCESS.format(
        amount=amount, receiver=receiver_tag)

    await client.send_message(message.channel, success_message)
