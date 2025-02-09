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


class PostStatus(str, enum.Enum):
    ACTIVE = 'active'
    ARCHIVE = 'archived'
    IN_PROCESS = 'in_process'


class PostTypes(enum.Enum):
    TRADE = 'trade'
    GIFT = 'gift'


class OfferScenarios(enum.Enum):
    SEND = 'send'
    END = 'end'
    ACCEPT = 'accept'
    REJECT = 'reject'
