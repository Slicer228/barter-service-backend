

def offerView(func):
    async def wrapper(*args):
        original = await func(*args)
        return original
    return wrapper