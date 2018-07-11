import database as main_db

import modules.base.models as base_models
import modules.base.helpers as base_helpers

import modules.raffle.models as raffle_models
import modules.raffle.settings as raffle_settings
import modules.raffle.helpers as raffle_helpers


@base_helpers.collate_args(0, 1)
async def admin_start_raffle(client, message, item_name, str_max_slots):
    # Validate argument
    error = base_helpers.validate_is_int(str_max_slots, True)

    if error is not None:
        await client.send_message(message.channel, error)
        return

    max_slots = int(str_max_slots)

    # Check if there is an ongoing raffle
    session = main_db.create_session()
    current_raffle = raffle_models.get_current_raffle(session)

    if current_raffle is not None:
        await client.send_message(
            message.channel,
            raffle_settings.ADMIN_START_RAFFLE_ERROR_RAFFLE_ONGOING)
        session.close()
        return

    # Start a new raffle
    raffle_models.create_raffle(session, item_name, max_slots)

    session.commit()
    session.close()

    success_message = raffle_settings.ADMIN_START_RAFFLE_SUCCESS.format(
        item_name=item_name, max_slots=max_slots)
    await client.send_message(message.channel, success_message)


@base_helpers.limit_command_arg(0)
async def admin_end_raffle(client, message):
    # Check if there is an ongoing raffle
    session = main_db.create_session()
    current_raffle = raffle_models.get_current_raffle(session)

    if current_raffle is None:
        await client.send_message(
            message.channel,
            raffle_settings.ADMIN_END_RAFFLE_ERROR_NO_RAFFLE_ONGOING)
        session.close()
        return

    item_name = current_raffle.item
    max_slots = current_raffle.max_slots

    # Pick a winner from the people who participated
    slots = raffle_models.get_raffle_slots(session, current_raffle.id)
    total_slots = raffle_models.get_total_raffle_slots_slots(
        session, current_raffle.id)
    winner = raffle_helpers.pick_winner(slots, total_slots)

    # Close the raffle
    current_raffle.status = raffle_settings.RAFFLE_DB_STATUS_CLOSED

    # Finalize the winner
    session.commit()

    # Notify winner and server
    if winner is None:
        winner_name = raffle_settings.ADMIN_END_RAFFLE_NO_WINNER_NAME
    else:
        winner_user = base_models.get_user(session, id=winner.user_id)
        winner_discord = await client.get_user_info(winner_user.snowflake)
        winner_name = base_helpers.get_identifier(winner_discord)

    success_message = raffle_settings.ADMIN_END_RAFFLE_SUCCESS.format(
        item_name=item_name, max_slots=max_slots, winner_name=winner_name)
    pm_message = raffle_settings.ADMIN_END_RAFFLE_PM.format(
        item_name=item_name)

    # Close early so that nothing happens
    session.close()

    await client.send_message(message.channel, success_message)
    await client.send_message(winner_discord, pm_message)
