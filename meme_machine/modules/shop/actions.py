import discord

import database as main_db

import modules.base.helpers as base_helpers
import modules.base.models as base_models

import modules.credits.models as credit_models
import modules.credits.helpers as credit_helpers

import modules.shop.settings as shop_settings
import modules.shop.models as shop_models


async def _shop(client, message, category_code, only_in_stock=True):
    session = main_db.create_session()

    category = shop_models.get_shop_category(
        session, category_code=category_code)

    if category is None:
        await client.send_message(
            message.channel, shop_settings.SHOP_ERROR_NO_SUCH_CATEGORY)
        return

    items = shop_models.get_shop_items(
        session, category_id=category.id)

    # Create the embed
    author_name = shop_settings.SHOP_TITLE.format(category_code=category_code)
    embed = discord.Embed(title=category.display_name,
                          color=int(category.color, 16))
    embed.set_author(name=author_name,
                     icon_url=shop_settings.SHOP_ALL_AUTHOR_ICON)
    embed.set_thumbnail(url=category.thumbnail_url)

    # Create the items
    for item in items:
        # Skip if there is not stock
        if only_in_stock and item.stock == 0:
            continue
        item_name = shop_settings.SHOP_DISPLAY_EACH_ITEM_NAME.format(
            name=item.name, stock=item.stock, code_name=item.code_name)
        item_value = shop_settings.SHOP_DISPLAY_EACH_ITEM_VALUE.format(
            cost=item.cost)
        embed.add_field(name=item_name, value=item_value, inline=False)

    session.close()

    # Display no items message if there are no items (or no items in stock)
    if not items:
        embed.add_field(name=shop_settings.SHOP_DISPLAY_NO_ITEMS,
                        value=".", inline=False)

    await client.send_message(message.channel, embed=embed)


@base_helpers.limit_command_arg(1)
async def shop(client, message, category_code):
    await _shop(client, message, category_code)


@base_helpers.limit_command_arg(1)
async def admin_shop(client, message, category_code):
    await _shop(client, message, category_code, False)


@base_helpers.limit_command_arg(0)
async def shops(client, message):
    embed = discord.Embed(title=shop_settings.SHOPS_TITLE,
                          color=shop_settings.SHOPS_COLOR)
    embed.set_author(name=shop_settings.SHOPS_TITLE,
                     icon_url=shop_settings.SHOP_ALL_AUTHOR_ICON)

    session = main_db.create_session()

    categories = shop_models.get_categories(session)
    for category in categories:
        value = shop_settings.SHOPS_VALUE.format(
            category_code=category.code_name)
        embed.add_field(name=category.display_name, value=value, inline=False)

    session.close()

    await client.send_message(message.channel, embed=embed)


@base_helpers.limit_command_arg(3)
async def admin_set_stock(client, message, category_code, item_code,
                          str_new_stock):
    # Validate arguments
    error = base_helpers.validate_is_int(str_new_stock, True)

    if error is not None:
        await client.send_message(message.channel, error)
        return

    session = main_db.create_session()
    item = shop_models.get_shop_item(session, category_code=category_code,
                                     item_code=item_code)

    # Error if there is no such item
    if item is None:
        await client.send_message(
            message.channel, shop_settings.ADMIN_SET_STOCK_ERROR_NO_SUCH_ITEM)
        session.close()
        return

    item.stock = str_new_stock
    item_name = item.name

    session.commit()
    session.close()

    success_message = shop_settings.ADMIN_SET_STOCK_SUCCESS.format(
        item_name=item_name, new_stock=str_new_stock)

    await client.send_message(message.channel, success_message)


@base_helpers.collate_args(2)
async def admin_update_category(client, message, category_code, update_type,
                                update_value):
    # Validate arguments
    # Check that the update type is a valid value
    error = None
    if update_type not in ["CODE", "THUMBNAIL_URL", "NAME", "COLOR"]:
        error = shop_settings.ADMIN_UPDATE_CATEGORY_ERROR_INVALID_TYPE
    elif update_type != "NAME" and " " in update_value:
        error = shop_settings.ADMIN_UPDATE_CATEGORY_SPACES_NOT_ALLOWED
    elif update_type == "COLOR":
        error = base_helpers.validate_is_hex(update_value, 6)

    if error is not None:
        await client.send_message(message.channel, error)
        return

    session = main_db.create_session()

    category = shop_models.get_shop_category(
        session, category_code=category_code)

    # Check if the category exists
    if category is None:
        await client.send_message(
            message.channel,
            shop_settings.SHOP_ERROR_NO_SUCH_CATEGORY)
        session.close()
        return

    # Update the value accordingly
    if update_type == "CODE":
        # Check if a category with that code already exists
        check_category = shop_models.get_shop_category(
            session, category_code=update_value)

        if check_category is not None:
            error_message = shop_settings.SHOP_ERROR_CATEGORY_EXISTS
            await client.send_message(message.channel, error_message)
            session.close()
            return

        category.code_name = update_value
    elif update_type == "THUMBNAIL_URL":
        category.thumbnail_url = update_value
    elif update_type == "NAME":
        category.display_name = update_value
    else:
        # update_value should be a color "0x000000"
        # Only take and store the 6 digits
        category.color = update_value[2:]

    session.commit()
    session.close()

    success_message = shop_settings.ADMIN_UPDATE_CATEGORY_SUCCESS.format(
        update_type=update_type.lower(), update_value=update_value)

    await client.send_message(message.channel, success_message)


@base_helpers.collate_args(1, 2)
async def admin_add_item(client, message, category_code, name,
                         str_cost, str_stock):
    # Validate arguments
    error = (credit_helpers.validate_credit_arg(str_cost) or
             base_helpers.validate_is_int(str_stock, True))

    if error is not None:
        await client.send_message(message.channel, error)
        return

    session = main_db.create_session()

    category = shop_models.get_shop_category(
        session, category_code=category_code)

    # Check if the category exists
    if category is None:
        await client.send_message(
            message.channel,
            shop_settings.SHOP_ERROR_NO_SUCH_CATEGORY)
        session.close()
        return

    # Check if item already exists in the category
    shop_item = shop_models.get_shop_item(
        session, category_id=category.id, item_name=name)

    if shop_item is not None:
        await client.send_message(
            message.channel,
            shop_settings.ADMIN_ADD_ITEM_ERROR_ITEM_ALREADY_EXISTS)
        session.close()
        return

    cost = int(str_cost)
    stock = int(str_stock)
    category_name = category.display_name

    shop_models.create_shop_item(session, category.id, name, cost, stock)

    session.commit()
    session.close()

    success_message = shop_settings.ADMIN_ADD_ITEM_SUCCESS.format(
        stock=stock, name=name, cost=cost, category_name=category_name)

    await client.send_message(message.channel, success_message)


@base_helpers.limit_command_arg(2)
async def admin_remove_item(client, message, category_code, item_code):
    # Validate arguments
    session = main_db.create_session()

    category = shop_models.get_shop_category(
        session, category_code=category_code)

    # Check if the category exists
    if category is None:
        await client.send_message(
            message.channel,
            shop_settings.SHOP_ERROR_NO_SUCH_CATEGORY)
        session.close()
        return

    # Check if item exists in the category
    shop_item = shop_models.get_shop_item(
        session, category_id=category.id, item_code=item_code)

    if shop_item is None:
        await client.send_message(
            message.channel,
            shop_settings.SHOP_ERROR_ITEM_DOES_NOT_EXIST)
        session.close()
        return

    # Check if item is in any open transaction
    transactions = shop_models.get_transactions(
        session, item_id=shop_item.id,
        status=shop_settings.TRANSACTION_DB_STATUS_PENDING)

    if transactions:
        await client.send_message(
            message.channel,
            shop_settings.ADMIN_REMOVE_ITEM_ERROR_ITEM_HAS_PENDING_TRANSACTION)
        session.close()
        return

    # Remove item
    session.delete(shop_item)

    item_name = shop_item.name
    category_name = category.display_name

    session.commit()
    session.close()

    success_message = shop_settings.ADMIN_REMOVE_ITEM_SUCCESS.format(
        name=item_name, category_name=category_name)

    await client.send_message(message.channel, success_message)


@base_helpers.collate_args(3)
async def admin_add_category(client, message, category_code, color,
                             thumbnail_url, display_name):
    # Validate arguments
    error = base_helpers.validate_is_hex(color, 6)

    if error is not None:
        await client.send_message(message.channel, error)
        return

    # Check that category code does not already exist
    session = main_db.create_session()

    category = shop_models.get_shop_category(
        session, category_code=category_code)

    if category is not None:
        await client.send_message(
            message.channel, shop_settings.SHOP_ERROR_CATEGORY_EXISTS)
        session.close()
        return

    shop_models.create_shop_category(session, display_name, category_code,
                                     color[2:], thumbnail_url)

    session.commit()
    session.close()

    success_message = shop_settings.ADMIN_ADD_CATEGORY_SUCCESS.format(
        name=display_name)

    await client.send_message(message.channel, success_message)


@base_helpers.limit_command_arg(1)
async def admin_remove_category(client, message, category_code):
    # Validate argument
    # Check that the category exists
    session = main_db.create_session()

    category = shop_models.get_shop_category(
        session, category_code=category_code)

    if category is None:
        await client.send_message(
            message.channel,
            shop_settings.SHOP_ERROR_CATEGORY_DOES_NOT_EXIST)
        session.close()
        return

    # Check that the category does not have any items
    items = shop_models.get_shop_items(session, category_id=category.id)
    if items:
        await client.send_message(
            message.channel,
            shop_settings.ADMIN_REMOVE_CATEGORY_ERROR_CATEGORY_HAS_ITEMS)
        session.close()
        return

    session.delete(category)

    category_name = category.display_name

    session.commit()
    session.close()

    success_message = shop_settings.ADMIN_REMOVE_CATEGORY_SUCCESS.format(
        name=category_name)

    await client.send_message(message.channel, success_message)


@base_helpers.limit_command_arg(3)
async def buy(client, message, category_code, item_code, str_amount):
    # Validate arguments
    error = base_helpers.validate_is_int(str_amount, True)

    if error is not None:
        await client.send_message(message.channel, error)
        return

    amount = int(str_amount)

    # Check that the amount is more than 0
    if amount == 0:
        await client.send_message(
            message.channel, shop_settings.BUY_ERROR_AMOUNT_ZERO)
        return

    # Check that the category exists
    session = main_db.create_session()

    category = shop_models.get_shop_category(
        session, category_code=category_code)

    if category is None:
        await client.send_message(
            message.channel,
            shop_settings.SHOP_ERROR_CATEGORY_DOES_NOT_EXIST)
        session.close()
        return

    # Check that the item exists in the category
    shop_item = shop_models.get_shop_item(session, category_id=category.id,
                                          item_code=item_code)

    if shop_item is None:
        await client.send_message(
            message.channel,
            shop_settings.SHOP_ERROR_ITEM_DOES_NOT_EXIST)
        session.close()
        return

    # Check if the user has enough credits to buy the item
    total_cost = shop_item.cost * amount

    sender_discord = message.author
    sender_user = base_models.get_or_create_user(session, sender_discord)
    sender_credit = credit_models.get_or_create_credit(session, sender_user.id)

    if sender_credit.credits < total_cost:
        error_message = shop_settings.BUY_ERROR_INSUFFICIENT_CREDITS.format(
            total_cost=total_cost, user_credits=sender_credit.credits)
        await client.send_message(message.channel, error_message)
        session.close()
        return

    # Create transaction
    transaction = shop_models.create_transaction(
        session, sender_user.id, shop_item.id, amount)

    # Deduct amount
    sender_credit.credits -= total_cost

    session.commit()

    user_identifier = base_helpers.get_identifier(sender_discord)

    sender_success_message = shop_settings.BUY_SENDER_SUCCESS.format(
        transaction_id=transaction.id, amount=amount, item_name=shop_item.name,
        total_cost=total_cost)
    purchase_order_message = shop_settings.BUY_PURCHASE_ORDER_SUCCESS.format(
        transaction_id=transaction.id, amount=amount, item_name=shop_item.name,
        total_cost=total_cost, user_identifier=user_identifier)

    session.close()

    # Send to initiator
    await client.send_message(message.channel, sender_success_message)
    # Send purchase order
    purchase_order_receiver = await client.get_user_info(
        shop_settings.BUY_PURCHASE_ORDER_DESTINATION)
    await client.send_message(purchase_order_receiver, purchase_order_message)


@base_helpers.limit_command_arg(1)
async def admin_trans_success(client, message, transaction_id):
    # Validate argument
    error = base_helpers.validate_is_int(transaction_id, True)

    if error is not None:
        await client.send_message(message.channel, error)
        return

    # Check that the transaction exists
    session = main_db.create_session()
    transaction = shop_models.get_transaction(session, transaction_id)

    if transaction is None:
        await client.send_message(
            message.channel,
            shop_settings.ADMIN_TRANS_ERROR_DOES_NOT_EXIST)
        session.close()
        return

    # Check that the transaction is still pending
    if transaction.status != shop_settings.TRANSACTION_DB_STATUS_PENDING:
        error_message = shop_settings.ADMIN_TRANS_ERROR_STATUS_ALREADY_SET \
            .format(current_status=transaction.status)
        await client.send_message(message.channel, error_message)
        session.close()
        return

    # Set the transaction status
    transaction.status = shop_settings.TRANSACTION_DB_STATUS_SUCCESS

    # Get the user initiator's discord user
    initiator_user = base_models.get_user(
        session, id=transaction.initiator_user_id)
    initiator_discord = await client.get_user_info(initiator_user.snowflake)

    # Get the item in the transaction
    shop_item = shop_models.get_shop_item(session, id=transaction.item_id)

    shop_item_name = shop_item.name
    amount = transaction.amount
    transaction_id = transaction.id

    session.commit()
    session.close()

    # Send the confirmation to the initiator
    confirm_message = shop_settings.ADMIN_TRANS_SUCCESS_INITIATOR.format(
        item_name=shop_item_name, amount=amount,
        transaction_id=transaction_id)
    await client.send_message(initiator_discord, confirm_message)

    success_message = shop_settings.ADMIN_TRANS_SUCCESS.format(
        item_name=shop_item_name, amount=amount,
        transaction_id=transaction_id)
    await client.send_message(message.channel, success_message)


@base_helpers.limit_command_arg(1)
async def admin_trans_fail(client, message, transaction_id):
    # Validate argument
    error = base_helpers.validate_is_int(transaction_id, True)

    if error is not None:
        await client.send_message(message.channel, error)
        return

    # Check that the transaction exists
    session = main_db.create_session()
    transaction = shop_models.get_transaction(session, transaction_id)

    if transaction is None:
        await client.send_message(
            message.channel,
            shop_settings.ADMIN_TRANS_ERROR_DOES_NOT_EXIST)
        session.close()
        return

    # Check that the transaction is still pending
    if transaction.status != shop_settings.TRANSACTION_DB_STATUS_PENDING:
        error_message = shop_settings.ADMIN_TRANS_ERROR_STATUS_ALREADY_SET \
            .format(current_status=transaction.status)
        await client.send_message(message.channel, error_message)
        session.close()
        return

    # Set the transaction status
    transaction.status = shop_settings.TRANSACTION_DB_STATUS_FAILED

    # Get the user initiator's discord user
    initiator_user = base_models.get_user(
        session, id=transaction.initiator_user_id)
    initiator_discord = await client.get_user_info(initiator_user.snowflake)

    # Get the item in the transaction
    shop_item = shop_models.get_shop_item(session, id=transaction.item_id)

    shop_item_name = shop_item.name
    amount = transaction.amount
    transaction_id = transaction.id

    total_cost = shop_item.cost * amount

    # Refund the credits
    initiator_credit = credit_models.get_credit(session, initiator_user.id)
    initiator_credit.credits += total_cost

    session.commit()
    session.close()

    # Send the failed message to the initiator
    fail_message = shop_settings.ADMIN_TRANS_FAILED_INITIATOR.format(
        item_name=shop_item_name, amount=amount,
        transaction_id=transaction_id, total_cost=total_cost)
    await client.send_message(initiator_discord, fail_message)

    success_message = shop_settings.ADMIN_TRANS_FAILED.format(
        item_name=shop_item_name, amount=amount,
        transaction_id=transaction_id)
    await client.send_message(message.channel, success_message)
