import enum


class TradeStatus(enum.Enum):
    IN_PROCESS = 'in_process'
    ACTIVE = 'active'
    FROZEN = 'frozen'
    ARCHIVED = 'archived'

class TradeTypes(enum.Enum):
    OFFER = 'offer'
    POST = 'post'


class PostStatus(enum.Enum):
    ACTIVE = 'active'
    ARCHIVE = 'archive'
    PROCESS = 'process'
