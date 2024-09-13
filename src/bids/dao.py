from src.bids.models import Bid, BidArchive, FeedBack
from src.dao.base import BaseDAO, ArchiveDAO


class BidDAO(BaseDAO, ArchiveDAO):
    model = Bid
    model_archive = BidArchive

class BidArchiveDAO(BaseDAO):
    model = BidArchive

class FeedbackDAO(BaseDAO):
    model = FeedBack