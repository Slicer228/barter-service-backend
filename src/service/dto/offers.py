

def offerView(func):
    async def wrapper(*args):
        original = await func(*args)
        if isinstance(original, dict):
            return original
        return original
    return wrapper