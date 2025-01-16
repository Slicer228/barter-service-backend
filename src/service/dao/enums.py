import enum


class TradeStatus(enum.Enum):
    IN_PROCESS = 'in_process'
    ACTIVE = 'active'
    FROZEN = 'frozen'
    ARCHIVED = 'archived'
    REJECTED = 'rejected'


class TradeTypes(enum.Enum):
    OFFER = 'offer'
    POST = 'post'


class PostStatus(enum.Enum):
    ACTIVE = 'active'
    ARCHIVE = 'archive'
    PROCESS = 'process'


class PostTypes(enum.Enum):
    TRADE = 'trade'
    GIFT = 'gift'
