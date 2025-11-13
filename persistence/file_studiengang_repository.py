import os
from typing import Any
from datetime import datetime, date
from decimal import Decimal

from persistence.istudiengang_repository_port import IStudiengangRepositoryPort
from persistence.json_adapter import JsonAdapter

from domain.studiengang import Studiengang
from domain.semester import Semester
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.zeitinvestition import Zeitinvestition
from domain.modulstatus import Modulstatus


class FileStudiengangRepository(IStudiengangRepositoryPort):
    
    def __init__(self, path: str, adapter: JsonAdapter):
        self.path = path
        self.adapter = adapter

    def load(self) -> Studiengang:
        if not os.path.exists(self.path):
            # Leeres Default-Dataset erzeugen
            return Studiengang(
                name="Softwareentwicklung B.Sc",
                ziel_abschlussjahre=3,
                ziel_durchschnitt=2.5,
                semester_liste=[]
            )

        raw = self.adapter.read(self.path)
        semester_liste = []

        for s in raw["semester_liste"]:
            module = []
            for m in s["module"]:
                ml = [
                    Pruefungsleistung(
                        art=p["art"],
                        note=Decimal(p["note"]),
                        versuch=p["versuch"],
                        datum=date.fromisoformat(p["datum"]),
                        status=Modulstatus(p["status"])
                    )
                    for p in m["pruefungsleistungen"]
                ]

                zl = [
                    Zeitinvestition(
                        datum=date.fromisoformat(z["datum"]),
                        stunden=z["stunden"],
                        beschreibung=z["beschreibung"]
                    )
                    for z in m["zeitinvestitionen"]
                ]

                module.append(Modul(
                    titel=m["titel"],
                    ects=m["ects"],
                    pruefungsleistungen=ml,
                    zeitinvestitionen=zl
                ))

            semester_liste.append(Semester(
                nummer=s["nummer"],
                ziel_arbeitsaufwand_h=s["ziel_arbeitsaufwand_h"],
                module=module
            ))

        return Studiengang(
            name=raw["name"],
            ziel_abschlussjahre=raw["ziel_abschlussjahre"],
            ziel_durchschnitt=raw["ziel_durchschnitt"],
            semester_liste=semester_liste
        )

    def save(self, studiengang: Studiengang) -> None:
        """Serialisiert das gesamte Objektmodell in JSON."""
        serialized = {
            "name": studiengang.name,
            "ziel_abschlussjahre": studiengang.ziel_abschlussjahre,
            "ziel_durchschnitt": studiengang.ziel_durchschnitt,
            "semester_liste": []
        }

        for s in studiengang.semester_liste:
            sem_dict = {
                "nummer": s.nummer,
                "ziel_arbeitsaufwand_h": s.ziel_arbeitsaufwand_h,
                "module": []
            }
            for m in s.module:
                sem_dict["module"].append({
                    "titel": m.titel,
                    "ects": m.ects,
                    "pruefungsleistungen": [
                        {
                            "art": p.art,
                            "note": str(p.note),
                            "versuch": p.versuch,
                            "datum": p.datum.isoformat(),
                            "status": p.status.value
                        }
                        for p in m.pruefungsleistungen
                    ],
                    "zeitinvestitionen": [
                        {
                            "datum": z.datum.isoformat(),
                            "stunden": z.stunden,
                            "beschreibung": z.beschreibung
                        }
                        for z in m.zeitinvestitionen
                    ]
                })
            serialized["semester_liste"].append(sem_dict)

        self.adapter.write(self.path, serialized)
