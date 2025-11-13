from dataclasses import dataclass, field
from decimal import Decimal
from typing import List
from domain.pruefungsleistung import Pruefungsleistung
from domain.zeitinvestition import Zeitinvestition
from domain.modulstatus import Modulstatus


@dataclass
class Modul:
    titel: str
    ects: int = 5
    pruefungsleistungen: List[Pruefungsleistung] = field(default_factory=list)
    zeitinvestitionen: List[Zeitinvestition] = field(default_factory=list)

    @property
    def aktuelle_note(self) -> Decimal | None:
        """Nimmt die beste bestandene Prüfungsleistung."""
        bestandene = [p for p in self.pruefungsleistungen if p.ist_bestanden()]
        if not bestandene:
            return None
        return min(bestandene, key=lambda x: x.note).note

    @property
    def aktueller_status(self) -> Modulstatus:
        """Abgeleitet aus den Prüfungsleistungen."""
        for p in self.pruefungsleistungen:
            if p.ist_bestanden():
                return Modulstatus.BESTANDEN
        return Modulstatus.NICHT_BESTANDEN

    @property
    def gesamt_zeitinvest(self) -> int:
        return sum(z.stunden for z in self.zeitinvestitionen)
