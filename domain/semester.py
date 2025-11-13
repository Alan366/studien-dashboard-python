from dataclasses import dataclass, field
from typing import List
from decimal import Decimal
from domain.modul import Modul


@dataclass
class Semester:
    nummer: int
    ziel_arbeitsaufwand_h: int = 600
    module: List[Modul] = field(default_factory=list)

    @property
    def berechne_durchschnittsnote(self) -> Decimal | None:
        noten = [m.aktuelle_note for m in self.module if m.aktuelle_note is not None]
        if not noten:
            return None
        return sum(noten) / len(noten)

    @property
    def berechne_ist_arbeitsaufwand(self) -> int:
        return sum(m.gesamt_zeitinvest for m in self.module)

    @property
    def zaehle_bestandene_module(self) -> int:
        return sum(1 for m in self.module if m.aktueller_status.name == "BESTANDEN")
