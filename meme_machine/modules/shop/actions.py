import discord

import database as main_db

import modules.base.helpers as base_helpers

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
