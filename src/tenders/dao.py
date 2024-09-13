from src.dao.base import BaseDAO, ArchiveDAO
from src.tenders.models import Tender, TenderArchive


class TenderDAO(BaseDAO, ArchiveDAO):
    model = Tender
    model_archive = TenderArchive

class TenderArchiveDAO(BaseDAO):
    model = TenderArchive