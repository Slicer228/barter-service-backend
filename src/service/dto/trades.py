

def trades_view(func):

    async def wrapper(*args):
        original = await func(*args)
        if original:
            if isinstance(original, list):
                return original if len(original) > 1 else original[0]
            return original
        else:
            return None
    return wrapper
