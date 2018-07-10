import database as main_db

import modules.base.helpers as base_helpers

import modules.raffle.models as raffle_models
import modules.raffle.settings as raffle_settings


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
