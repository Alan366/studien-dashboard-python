from dataclasses import dataclass, field
from typing import List
from decimal import Decimal
from domain.semester import Semester


@dataclass
class Studiengang:
    name: str
    ziel_abschlussjahre: int
    ziel_durchschnitt: float
    semester_liste: List[Semester] = field(default_factory=list)

    def gesamtdurchschnitt(self) -> Decimal | None:
        noten = []
        for sem in self.semester_liste:
            if sem.berechne_durchschnittsnote is not None:
                noten.append(sem.berechne_durchschnittsnote)
        if not noten:
            return None
        return sum(noten) / len(noten)

    def gesamt_arbeitsstunden(self) -> int:
        return sum(s.berechne_ist_arbeitsaufwand for s in self.semester_liste)

    def fortschritt_prozent(self) -> float:
        total_modules = sum(len(s.module) for s in self.semester_liste)
        passed = sum(s.zaehle_bestandene_module for s in self.semester_liste)
        if total_modules == 0:
            return 0.0
        return (passed / total_modules) * 100
