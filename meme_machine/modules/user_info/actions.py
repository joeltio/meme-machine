import database as maindb

import modules.base.models as base_models
import modules.base.helpers as base_helpers

import modules.credits.models as credit_models

import modules.raffle.models as raffle_models

import modules.user_info.models as user_info_models
import modules.user_info.settings as user_info_settings


@base_helpers.limit_command_arg(0)
async def profile(client, message):
    profile_message = user_info_settings.PROFILE_DISPLAY_HEADER + "\n"

    session = maindb.create_session()

    # User
    sender_discord = message.author
    sender_user = base_models.get_or_create_user(session, sender_discord)

    # Credits
    sender_credit = credit_models.get_or_create_credit(session, sender_user.id)
    profile_message += user_info_settings.PROFILE_DISPLAY_CREDIT.format(
        credits=sender_credit.credits) + "\n"

    # Raffles
    current_raffle = raffle_models.get_raffle(session)
    if current_raffle is not None:
        sender_raffle_slots = raffle_models.get_raffle_slot(
            session, sender_user.id, current_raffle.id)

        sender_num_slots = sender_raffle_slots.slots or 0

        profile_message += user_info_settings.PROFILE_DISPLAY_RAFFLE.format(
            user_slots=sender_num_slots, max_slots=current_raffle.max_slots)
        profile_message += "\n"
    else:
        # No current raffle
        profile_message += \
            user_info_settings.PROFILE_DISPLAY_NO_CURRENT_RAFFLES + "\n"

    # Steam Profile Url
    steam_url = user_info_models.get_steam_profile(session, sender_user.id) \
        or user_info_settings.PROFILE_DISPLAY_NO_STEAM_URL
    profile_message += user_info_settings.PROFILE_DISPLAY_STEAM_URL.format(
        steam_url=steam_url) + "\n"

    session.close()

    profile_message += user_info_settings.PROFILE_DISPLAY_FOOTER
    await client.send_message(message.channel, profile_message)
