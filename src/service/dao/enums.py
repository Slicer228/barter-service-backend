import enum


class TradeTypes(enum.Enum):
    OFFER = 'offer'
    POST = 'post'


class PostStatus(enum.Enum):
    ACTIVE = 'active'
    ARCHIVE = 'archive'
    PROCESS = 'process'
