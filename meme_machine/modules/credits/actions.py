import random
from datetime import datetime, timedelta

import database as main_db

import modules.base.helpers as base_helpers
import modules.base.models as base_models

import modules.credits.models as credit_models
import modules.credits.settings as credit_settings
import modules.credits.helpers as credit_helpers


@base_helpers.limit_command_arg(2)
async def donate(client, message, receiver_tag, str_amount):
    # Validate incoming arguments
    error = (credit_helpers.validate_credit_arg(str_amount) or
             base_helpers.validate_num_of_mentions(message.mentions, 1))

    if error is None:
        # Check for self donation
        if message.author.mention == receiver_tag:
            await client.send_message(
                message.channel, credit_settings.DONATE_ERROR_SELF_DONATE)
            return
    else:
        await client.send_message(message.channel, error)
        return

    amount = int(str_amount)

    sender_discord = message.author
    receiver_discord = message.mentions[0]

    # Start a session
    session = main_db.create_session()

    # 1. Create both users if they do not already exist
    sender_user = base_models.get_or_create_user(session, sender_discord)
    receiver_user = base_models.get_or_create_user(session, receiver_discord)

    # 2. Create their credit records if they do not already exist
    sender_credit = credit_models.get_or_create_credit(session, sender_user.id)
    receiver_credit = credit_models.get_or_create_credit(
        session, receiver_user.id)

    # 3. Check if there is enough credits in the sending user
    if sender_credit.credits < amount:
        await client.send_message(
            message.channel, credit_settings.DONATE_ERROR_INSUFFICIENT_CREDITS)

        session.commit()
        session.close()
        return

    # 4. Transfer the credits
    sender_credit.credits -= amount
    receiver_credit.credits += amount

    # 5. Commit and close the session
    session.commit()
    session.close()

    success_message = credit_settings.DONATE_SUCCESS.format(
        amount=amount, receiver=receiver_tag)
    await client.send_message(message.channel, success_message)


@base_helpers.limit_command_arg(2)
async def admin_add(client, message, receiver_tag, str_amount):
    error = (credit_helpers.validate_credit_arg(str_amount) or
             base_helpers.validate_num_of_mentions(message.mentions, 1))

    if error is not None:
        await client.send_message(message.channel, error)
        return

    amount = int(str_amount)
    receiver_discord = message.mentions[0]

    # Start a session
    session = main_db.create_session()

    receiver_user = credit_models.get_or_create_user(session, receiver_discord)
    receiver_credit = credit_models.get_or_create_credit(
        session, receiver_user.id)

    # Increase the credit amount
    receiver_credit.credits += amount

    session.commit()
    session.close()

    success_message = credit_settings.ADMIN_ADD_SUCCESS.format(
        amount=str_amount, receiver=receiver_tag)

    await client.send_message(message.channel, success_message)


@base_helpers.limit_command_arg(2)
async def admin_remove(client, message, receiver_tag, str_amount):
    error = (credit_helpers.validate_credit_arg(str_amount) or
             base_helpers.validate_num_of_mentions(message.mentions, 1))

    if error is not None:
        await client.send_message(message.channel, error)
        return

    amount = int(str_amount)
    receiver_discord = message.mentions[0]

    # Start a session
    session = main_db.create_session()

    receiver_user = credit_models.get_or_create_user(session, receiver_discord)
    receiver_credit = credit_models.get_or_create_credit(
        session, receiver_user.id)

    # Find out how much should be deducted
    deduction = min(receiver_credit.credits, amount)

    # Deduct receiver's credit
    receiver_credit.credits -= deduction

    session.commit()
    session.close()

    success_message = credit_settings.ADMIN_REMOVE_SUCCESS.format(
        amount=deduction, receiver=receiver_tag)

    await client.send_message(message.channel, success_message)


@base_helpers.limit_command_arg(0)
async def daily(client, message):
    # Start a session
    session = main_db.create_session()

    # Get or create a user
    sender_discord = message.author
    sender_user = base_models.get_or_create_user(session, sender_discord)

    # Get or create credit action
    sender_credit_action = credit_models.get_or_create_credit_action(
        session, sender_user.id)

    # Check if the user is elgible for daily, i.e. current time after
    # next_daily
    time_left = sender_credit_action.next_daily - datetime.now()
    time_left_seconds = time_left.total_seconds()

    if time_left_seconds > 0:
        # Not time yet
        if time_left_seconds < 60:
            # Less than a minute
            result_message = credit_settings.DAILY_SECONDS_LEFT.format(
                seconds=int(time_left_seconds))
        elif time_left_seconds < 360:
            # Less than an hour
            result_message = credit_settings.DAILY_MINUTES_LEFT.format(
                minutes=int(time_left_seconds//60))
        else:
            # Less than a day
            hours = int(time_left_seconds//3600)
            minutes = int((time_left_seconds - hours*3600)//60)
            result_message = credit_settings.DAILY_HOURS_AND_MINUTES_LEFT \
                .format(hours=hours, minutes=minutes)
    else:
        # Get daily max and min
        daily_min_config, daily_max_config = \
            credit_models.get_or_create_daily_range(session)
        daily_min = int(daily_min_config.value)
        daily_max = int(daily_max_config.value)

        # Give the daily
        amount = random.randint(daily_min, daily_max)

        sender_credit = credit_models.get_or_create_credit(
            session, sender_user.id)
        sender_credit.credits += amount

        # Update next_daily
        sender_credit_action.next_daily = datetime.now() + timedelta(days=1)

        result_message = credit_settings.DAILY_SUCCESS.format(
            amount=amount, mention=sender_discord.mention)

    session.commit()
    session.close()

    await client.send_message(message.channel, result_message)


@base_helpers.limit_command_arg(2)
async def admin_daily_amt(client, message, str_new_min, str_new_max):
    # Validate arguments
    error = (credit_helpers.validate_credit_arg(str_new_min) or
             credit_helpers.validate_credit_arg(str_new_max) or
             credit_helpers.validate_credit_range(
                 int(str_new_min), int(str_new_max)))

    if error is not None:
        await client.send_message(message.channel, error)
        return

    session = main_db.create_session()

    daily_min_config, daily_max_config = \
        credit_models.get_or_create_daily_range(session)
    daily_min_config.value = str_new_min
    daily_max_config.value = str_new_max

    session.commit()
    session.close()

    success_message = credit_settings.ADMIN_DAILY_AMT_SUCCESS.format(
        start=str_new_min, end=str_new_max)

    await client.send_message(message.channel, success_message)


async def hook_user_activity(client, message):
    session = main_db.create_session()

    discord_user = message.author
    user = base_models.get_or_create_user(session, discord_user)

    # Get the next reward time
    credit_action = credit_models.get_or_create_credit_action(
        session, user.id)

    time_left = credit_action.next_active - datetime.now()

    # Stop if it is not time yet
    if time_left.total_seconds() >= 0:
        return

    # Get reward amount
    reward_min_config, reward_max_config = \
        credit_models.get_or_create_randpp_amt_range(session)

    amount = random.randint(int(reward_min_config.value),
                            int(reward_max_config.value))

    # Get next reward time
    time_min_config, time_max_config = \
        credit_models.get_or_create_randpp_time_range(session)

    time_interval = random.randint(int(time_min_config.value),
                                   int(time_max_config.value))

    # Give the reward amount
    user_credit = credit_models.get_or_create_credit(session, user.id)
    user_credit.credits += amount

    # Set the next reward time
    credit_action.next_active = \
        datetime.now() + timedelta(minutes=time_interval)

    session.commit()

    success_message = credit_settings.HOOK_USER_ACTIVITY_SUCCESS.format(
        amount=amount, mention=discord_user.mention)
    await client.send_message(message.channel, success_message)
