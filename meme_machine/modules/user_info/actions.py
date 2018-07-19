import discord

import database as maindb

import modules.base.models as base_models
import modules.base.helpers as base_helpers
import modules.base.settings as base_settings

import modules.credits.models as credit_models

import modules.raffle.models as raffle_models

import modules.user_info.models as user_info_models
import modules.user_info.settings as user_info_settings


@base_helpers.limit_command_arg(0)
async def profile(client, message):
    session = maindb.create_session()

    # User
    sender_discord = message.author
    sender_user = base_models.get_or_create_user(session, sender_discord)

    embed = discord.Embed(
        title=sender_discord.name,
        color=user_info_settings.PROFILE_DISPLAY_COLOR)
    embed.set_author(name=user_info_settings.PROFILE_DISPLAY_TITLE,
                     icon_url=base_settings.EMBED_AUTHOR_ICON)
    embed.set_thumbnail(
        url=sender_discord.avatar_url or sender_discord.default_avatar_url)

    # Credits
    sender_credit = credit_models.get_or_create_credit(session, sender_user.id)

    # Add the credits field to the embed
    embed_credit_value = user_info_settings.PROFILE_DISPLAY_CREDIT_VALUE \
        .format(credits=sender_credit.credits)
    embed.add_field(
        name=user_info_settings.PROFILE_DISPLAY_CREDIT_NAME,
        value=embed_credit_value, inline=False)

    # Raffles
    current_raffle = raffle_models.get_raffle(session)
    if current_raffle is not None:
        sender_raffle_slots = raffle_models.get_raffle_slot(
            session, sender_user.id, current_raffle.id)

        sender_num_slots = sender_raffle_slots.slots or 0

        embed_raffle_value = user_info_settings.PROFILE_DISPLAY_RAFFLE_VALUE \
            .format(user_slots=sender_num_slots,
                    max_slots=current_raffle.max_slots)
    else:
        # No current raffle
        embed_raffle_value = \
            user_info_settings.PROFILE_DISPLAY_NO_CURRENT_RAFFLES

    embed.add_field(
        name=user_info_settings.PROFILE_DISPLAY_RAFFLE_NAME,
        value=embed_raffle_value, inline=False)

    # Steam Profile Url
    steam_url = user_info_models.get_steam_profile(session, sender_user.id) \
        or user_info_settings.PROFILE_DISPLAY_NO_STEAM_URL

    embed_steam_url_value = \
        user_info_settings.PROFILE_DISPLAY_STEAM_URL_VALUE.format(
            steam_url=steam_url)
    embed.add_field(
        name=user_info_settings.PROFILE_DISPLAY_STEAM_URL_NAME,
        value=embed_steam_url_value, inline=False)

    session.close()

    await client.send_message(message.channel, embed=embed)


@base_helpers.limit_command_arg(1)
async def set_steam_profile(client, message, steam_profile_url):
    # Validate steam profile url
    if not steam_profile_url.startswith("https://steamcommunity.com/id/"):
        await client.send_message(
            message.channel,
            user_info_settings.SET_STEAM_PROFILE_ERROR_INVALID)
        return

    session = maindb.create_session()

    # Get the user
    sender_discord = message.author
    sender_user = base_models.get_or_create_user(session, sender_discord)

    user_info_models.set_steam_profile(
        session, sender_user.id, steam_profile_url)

    session.commit()
    session.close()

    success_message = user_info_settings.SET_STEAM_PROFILE_SUCCESS.format(
        new_profile_url=steam_profile_url)
    await client.send_message(message.channel, success_message)
