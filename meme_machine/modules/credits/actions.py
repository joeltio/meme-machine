from datetime import datetime, timedelta
from database import create_session
from modules.base.helpers import (limit_command_arg, validate_num_of_mentions,
                                  first)
import random

from modules.base.models import get_or_create_user
from modules.credits.models import (get_or_create_credit,
                                    get_or_create_credit_action,
                                    get_or_create_daily_range)
from modules.credits.settings import *
from modules.credits.helpers import validate_credit_arg


@limit_command_arg(2)
async def donate(client, message, receiver_tag, str_amount):
    # Validate incoming arguments
    validations = [
        validate_credit_arg(str_amount),
        validate_num_of_mentions(message.mentions, 1),
    ]
    error = first(lambda x: x is not None, validations)

    if error is None:
        # Check for self donation
        if message.author.mention == receiver_tag:
            await client.send_message(message.channel,
                                      DONATE_ERROR_SELF_DONATE)
            return
    else:
        await client.send_message(message.channel, error)
        return

    amount = int(str_amount)

    sender_discord = message.author
    receiver_discord = message.mentions[0]

    # Start a session
    session = create_session()

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
    validations = [
        validate_credit_arg(str_amount),
        validate_num_of_mentions(message.mentions, 1),
    ]
    error = first(lambda x: x is not None, validations)

    if error is not None:
        await client.send_message(message.channel, error)
        return

    amount = int(str_amount)
    receiver_discord = message.mentions[0]

    # Start a session
    session = create_session()

    receiver_user = get_or_create_user(session, receiver_discord)
    receiver_credit = get_or_create_credit(session, receiver_user.id)

    # Increase the credit amount
    receiver_credit.credits += amount

    session.commit()
    session.close()

    success_message = ADMIN_ADD_SUCCESS.format(
        amount=str_amount, receiver=receiver_tag)

    await client.send_message(message.channel, success_message)


@limit_command_arg(2)
async def admin_remove(client, message, receiver_tag, str_amount):
    validations = [
        validate_credit_arg(str_amount),
        validate_num_of_mentions(message.mentions, 1),
    ]
    error = first(lambda x: x is not None, validations)

    if error is not None:
        await client.send_message(message.channel, error)
        return

    amount = int(str_amount)
    receiver_discord = message.mentions[0]

    # Start a session
    session = create_session()

    receiver_user = get_or_create_user(session, receiver_discord)
    receiver_credit = get_or_create_credit(session, receiver_user.id)

    # Find out how much should be deducted
    deduction = min(receiver_credit.credits, amount)

    # Deduct receiver's credit
    receiver_credit.credits -= deduction

    session.commit()
    session.close()

    success_message = ADMIN_REMOVE_SUCCESS.format(
        amount=deduction, receiver=receiver_tag)

    await client.send_message(message.channel, success_message)


@limit_command_arg(0)
async def daily(client, message):
    # Start a session
    session = create_session()

    # Get or create a user
    sender_discord = message.author
    sender_user = get_or_create_user(session, sender_discord)

    # Get or create credit action
    sender_credit_action = get_or_create_credit_action(session, sender_user.id)

    # Check if the user is elgible for daily, i.e. current time after
    # next_daily
    time_left = sender_credit_action.next_daily - datetime.now()
    time_left_seconds = time_left.total_seconds()

    if time_left_seconds > 0:
        # Not time yet
        if time_left_seconds < 60:
            # Less than a minute
            result_message = DAILY_SECONDS_LEFT.format(
                seconds=int(time_left_seconds))
        elif time_left_seconds < 360:
            # Less than an hour
            result_message = DAILY_MINUTES_LEFT.format(
                minutes=int(time_left_seconds//60))
        else:
            # Less than a day
            hours = int(time_left_seconds//3600)
            minutes = int((time_left_seconds - hours*3600)//60)
            result_message = DAILY_HOURS_AND_MINUTES_LEFT.format(
                hours=hours, minutes=minutes)
    else:
        # Get daily max and min
        daily_min, daily_max = get_or_create_daily_range(session)

        # Give the daily
        amount = random.randint(daily_min, daily_max)

        sender_credit = get_or_create_credit(session, sender_user.id)
        sender_credit.credits += amount

        # Update next_daily
        sender_credit_action.next_daily = datetime.now() + timedelta(days=1)

        result_message = DAILY_SUCCESS.format(amount=amount)

    session.commit()
    session.close()

    await client.send_message(message.channel, result_message)
