
class NotFound(Exception):
    def __str__(self):
        return "Resourse you're looking for doesn't exists"

class NoAccess(Exception):
    def __str__(self):
        return "Resourse you're looking for doesn't accesible for you"