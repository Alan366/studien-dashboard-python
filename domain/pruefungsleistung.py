from dataclasses import dataclass
from decimal import Decimal
from domain.modulstatus import Modulstatus
import datetime


@dataclass
class Pruefungsleistung:
    art: str
    note: Decimal
    versuch: int
    datum: datetime.date
    status: Modulstatus

    def ist_bestanden(self) -> bool:
        """Ein Versuch ist bestanden, wenn Note <= 4.0 und Status BESTANDEN."""
        return self.note <= Decimal("4.0") and self.status == Modulstatus.BESTANDEN
