

def offerView(func):
    async def wrapper(*args):
        original = await func(*args)
        if original:
            return original
        else:
            return None
    return wrapper