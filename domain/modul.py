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
        """
        Note für die Berechnung:
        - wenn es Prüfungsleistungen gibt -> NOTE der letzten Prüfungsleistung
        - sonst None
        """
        if not self.pruefungsleistungen:
            return None
        return self.pruefungsleistungen[-1].note

    @property
    def aktueller_status(self) -> Modulstatus | None:
        """
        - Keine Prüfungsleistung -> None (Status bleibt in GUI leer)
        - Mindestens eine bestandene PL -> BESTANDEN
        - Nur nicht bestandene PL -> NICHT_BESTANDEN
        """
        if not self.pruefungsleistungen:
            return None

        for p in self.pruefungsleistungen:
            if p.ist_bestanden():
                return Modulstatus.BESTANDEN

        return Modulstatus.NICHT_BESTANDEN


    @property
    def gesamt_zeitinvest(self) -> int:
        return sum(z.stunden for z in self.zeitinvestitionen)
