import discord

import database as main_db

import modules.base.helpers as base_helpers

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
            error_message = shop_settings.ADMIN_UPDATE_CATEGORY_CODE_EXISTS
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
            shop_settings.ADMIN_REMOVE_ITEM_ERROR_ITEM_DOES_NOT_EXIST)
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
