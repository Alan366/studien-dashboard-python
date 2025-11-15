from dataclasses import dataclass, field
from typing import List
from decimal import Decimal

from domain.modul import Modul
from domain.modulstatus import Modulstatus


@dataclass
class Semester:
    nummer: int
    ziel_arbeitsaufwand_h: int = 600   # festes Ziel
    module: List[Modul] = field(default_factory=list)

    @property
    def berechne_durchschnittsnote(self) -> Decimal | None:
        """
        Durchschnitt über alle Module mit Note
        (auch nicht bestandene mit 5,0 fließen ein).
        """
        noten = [m.aktuelle_note for m in self.module if m.aktuelle_note is not None]
        if not noten:
            return None
        return sum(noten) / len(noten)

    @property
    def berechne_ist_arbeitsaufwand(self) -> int:
        """Summe der Stunden aus allen Zeitinvestitionen im Semester."""
        return sum(m.gesamt_zeitinvest for m in self.module)

    @property
    def zaehle_bestandene_module(self) -> int:
        """Zählt Module mit Status BESTANDEN."""
        return sum(1 for m in self.module if m.aktueller_status == Modulstatus.BESTANDEN)
