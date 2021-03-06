# Automatically generated by pb2py
from .. import protobuf as p
if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None
from .NEMMosaic import NEMMosaic


class NEMTransfer(p.MessageType):
    FIELDS = {
        1: ('recipient', p.UnicodeType, 0),
        2: ('amount', p.UVarintType, 0),
        3: ('payload', p.BytesType, 0),
        4: ('public_key', p.BytesType, 0),
        5: ('mosaics', NEMMosaic, p.FLAG_REPEATED),
    }

    def __init__(
        self,
        recipient: str = None,
        amount: int = None,
        payload: bytes = None,
        public_key: bytes = None,
        mosaics: List[NEMMosaic] = None
    ) -> None:
        self.recipient = recipient
        self.amount = amount
        self.payload = payload
        self.public_key = public_key
        self.mosaics = mosaics if mosaics is not None else []
