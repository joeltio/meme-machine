def validate_steam_url(url):
    """Checks whether a url is a valid steam profile url

    :param url: The url to validate
    :returns: bool -- Whether the steam url is valid."""
    prefixes = [
        "https://steamcommunity.com/id/",
        "https://steamcommunity.com/profiles/"
    ]
    return any(map(lambda x: url.startswith(x), prefixes))
