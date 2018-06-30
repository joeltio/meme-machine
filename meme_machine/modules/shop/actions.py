import database as main_db

import modules.base.helpers as base_helpers

import modules.shop.settings as shop_settings
import modules.shop.models as shop_models
import modules.shop.helpers as shop_helpers


async def _shop(client, message, only_in_stock=True):
    session = main_db.create_session()
    organized_items = shop_helpers.get_and_organize_items(session)

    all_items = []
    for cat_id, items in organized_items.items():
        category = shop_models.get_shop_category(session, id=cat_id)

        # Create the text for each category
        category_text = shop_settings.SHOP_DISPLAY_EACH_CATEGORY.format(
            name=category.display_name, code_name=category.code_name) + "\n"

        # Create the text for the items section of the category
        items_text = ""
        for item in items:
            # Skip if there is not stock
            if only_in_stock and item.stock == 0:
                continue

            item_text = shop_settings.SHOP_DISPLAY_EACH_ITEM.format(
                name=item.name, code_name=item.code_name,
                cost=item.cost, stock=item.stock)

            items_text += item_text + "\n"

        # Add the category into the display message only if there are items
        if items_text:
            all_items.append(category_text + items_text)

    session.close()

    # Display no items message if there are no items (or no items in stock)
    if not all_items:
        await client.send_message(
            message.channel, shop_settings.SHOP_DISPLAY_NO_ITEMS)
        return

    # Join the items with the category separator
    category_separator = shop_settings.SHOP_DISPLAY_CATEGORY_SEP + "\n"
    all_item_texts = category_separator.join(all_items)

    # Put everything together
    shop_display_message = shop_settings.SHOP_DISPLAY_HEADER + "\n"
    shop_display_message += all_item_texts
    shop_display_message += shop_settings.SHOP_DISPLAY_FOOTER

    await client.send_message(message.channel, shop_display_message)


@base_helpers.limit_command_arg(0)
async def shop(client, message):
    await _shop(client, message)


@base_helpers.limit_command_arg(0)
async def admin_shop(client, message):
    await _shop(client, message, False)


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
