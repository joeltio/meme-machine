"""Shop display layout example result:
<HEADER>
<EACH_CATEGORY>
<EACH_ITEM>
<EACH_ITEM>
<EACH_ITEM>
<CATEGORY_SEP>
<EACH_CATEGORY>
<EACH_ITEM>
<EACH_ITEM>
<EACH_ITEM>
<CATEGORY_SEP>
<EACH_CATEGORY>
<EACH_ITEM>
<EACH_ITEM>
<EACH_ITEM>
<FOOTER>

Required values to be formatted:
SHOP_DISPLAY_EACH_ITEM - {name}, {code_name}, {cost}, {stock}
SHOP_DISPLAY_EACH_CATEGRY - {name}, {code_name}

For example:
SHOP_DISPLAY_EACH_ITEM = "{name} [id: {code_name}] - {cost}PP"
SHOP_DISPLAY_EACH_CATEGORY = "{name} [id: {code_name}]"

If there are no items (or all items are not in stock), only the
SHOP_DISPLAY_NO_ITEMS will displayed.
"""
SHOP_DISPLAY_HEADER = "```Welcome to the PP Shop!\n"
SHOP_DISPLAY_EACH_CATEGORY = "{name} (id: {code_name}):"
SHOP_DISPLAY_EACH_ITEM = "{stock:<3}x{name} [id: {code_name}] - {cost}PP"
SHOP_DISPLAY_CATEGORY_SEP = "\n"
SHOP_DISPLAY_FOOTER = "```"
SHOP_DISPLAY_NO_ITEMS = ("Looks like there are no items right now. Check back "
                         "again later!")
