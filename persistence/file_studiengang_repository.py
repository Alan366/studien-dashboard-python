# persistence/file_studiengang_repository.py
import os
from datetime import date
from decimal import Decimal

from persistence.istudiengang_repository_port import IStudiengangRepositoryPort
from persistence.json_adapter import JsonAdapter
from persistence.excel_adapter import ExcelAdapter

from domain.studiengang import Studiengang
from domain.semester import Semester
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.zeitinvestition import Zeitinvestition
from domain.modulstatus import Modulstatus


class FileStudiengangRepository(IStudiengangRepositoryPort):
    """
    Lädt / speichert den Studiengang in JSON.
    Wenn noch keine JSON existiert, werden die Module aus module.xlsx importiert.
    """

    def __init__(self, json_path: str, json_adapter: JsonAdapter,
                 excel_path: str, excel_adapter: ExcelAdapter):
        self.json_path = json_path
        self.json_adapter = json_adapter
        self.excel_path = excel_path
        self.excel_adapter = excel_adapter

    # ---------- Public API ----------

    def load(self) -> Studiengang:
        # Wenn JSON existiert -> direkt laden
        if os.path.exists(self.json_path):
            return self._load_from_json()

        # Sonst: aus Excel initialisieren
        if not os.path.exists(self.excel_path):
            raise FileNotFoundError(
                f"Excel-Datei '{self.excel_path}' nicht gefunden. "
                f"Erstelle sie mit create_module_excel.py oder manuell."
            )

        return self._create_from_excel()

    def save(self, studiengang: Studiengang) -> None:
        data = {
            "name": studiengang.name,
            "ziel_abschlussjahre": studiengang.ziel_abschlussjahre,
            "ziel_durchschnitt": studiengang.ziel_durchschnitt,
            "semester_liste": [],
        }

        for s in studiengang.semester_liste:
            sem_dict = {
                "nummer": s.nummer,
                "ziel_arbeitsaufwand_h": s.ziel_arbeitsaufwand_h,
                "module": [],
            }
            for m in s.module:
                sem_dict["module"].append(
                    {
                        "titel": m.titel,
                        "ects": m.ects,
                        "pruefungsleistungen": [
                            {
                                "art": p.art,
                                "note": str(p.note),
                                "versuch": p.versuch,
                                "datum": p.datum.isoformat(),
                                "status": p.status.value,
                            }
                            for p in m.pruefungsleistungen
                        ],
                        "zeitinvestitionen": [
                            {
                                "datum": z.datum.isoformat(),
                                "stunden": z.stunden,
                                "beschreibung": z.beschreibung,
                            }
                            for z in m.zeitinvestitionen
                        ],
                    }
                )
            data["semester_liste"].append(sem_dict)

        self.json_adapter.write(self.json_path, data)

    # ---------- intern: JSON laden ----------

    def _load_from_json(self) -> Studiengang:
        raw = self.json_adapter.read(self.json_path)
        semester_liste = []

        for s in raw["semester_liste"]:
            module = []
            for m in s["module"]:
                pruefungsleistungen = [
                    Pruefungsleistung(
                        art=p["art"],
                        note=Decimal(p["note"]),
                        versuch=p["versuch"],
                        datum=date.fromisoformat(p["datum"]),
                        status=Modulstatus(p["status"]),
                    )
                    for p in m["pruefungsleistungen"]
                ]

                zeitinvestitionen = [
                    Zeitinvestition(
                        datum=date.fromisoformat(z["datum"]),
                        stunden=z["stunden"],
                        beschreibung=z["beschreibung"],
                    )
                    for z in m["zeitinvestitionen"]
                ]

                module.append(
                    Modul(
                        titel=m["titel"],
                        ects=m["ects"],
                        pruefungsleistungen=pruefungsleistungen,
                        zeitinvestitionen=zeitinvestitionen,
                    )
                )

            semester_liste.append(
                Semester(
                    nummer=s["nummer"],
                    ziel_arbeitsaufwand_h=s["ziel_arbeitsaufwand_h"],
                    module=module,
                )
            )

        return Studiengang(
            name=raw["name"],
            ziel_abschlussjahre=raw["ziel_abschlussjahre"],
            ziel_durchschnitt=raw["ziel_durchschnitt"],
            semester_liste=semester_liste,
        )

        # ---------- intern: aus Excel initialisieren ----------

     # ---------- intern: aus Excel initialisieren ----------

    def _create_from_excel(self) -> Studiengang:
        """
        Initialer Aufbau:
        - Modulliste kommt aus module.xlsx (nur Namen + Semester).
        - Alle Noten/Zeiten/Status sind leer und werden später per GUI gesetzt.
        - Ziele (Durchschnitt 2,5 / 600h) sind fest hinterlegt.
        """
        mapping = self.excel_adapter.read_module_list(self.excel_path)

        semester_liste: list[Semester] = []

        for sem_nr in range(1, 7):
            namen = mapping.get(sem_nr, [])
            module = [
                Modul(
                    titel=name,
                    ects=5,
                    pruefungsleistungen=[],
                    zeitinvestitionen=[],
                )
                for name in namen
            ]

            semester_liste.append(
                Semester(
                    nummer=sem_nr,
                    ziel_arbeitsaufwand_h=600,
                    module=module,
                )
            )

        return Studiengang(
            name="Cyber Security Bachelor",
            ziel_abschlussjahre=3,
            ziel_durchschnitt=2.5,
            semester_liste=semester_liste,
        )
