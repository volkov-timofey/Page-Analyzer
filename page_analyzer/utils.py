import validators


def is_valid_url(url: str) -> bool:
    '''
    Castom validator for url
    '''
    if len(url) <= 255:
        return validators.url(url)

    return False
