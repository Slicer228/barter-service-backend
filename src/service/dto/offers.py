from src.exception_handlers import error_handler_offers


def offer_view(func):

    @error_handler_offers
    async def wrapper(*args):
        original = await func(*args)
        if original:
            if isinstance(original, list):
                return original if len(original) > 1 else original[0]
            return original
        else:
            return None
    return wrapper
