# controller/dashboard_controller.py

from decimal import Decimal
import datetime
from typing import Optional

from domain.semester import Semester
from domain.modul import Modul
from domain.modulstatus import Modulstatus
from domain.pruefungsleistung import Pruefungsleistung
from domain.zeitinvestition import Zeitinvestition


class DashboardController:
    """
    Verbindet GUI und Domäne:
    - liefert Kennzahlen für die Anzeige
    - übernimmt Eingaben (Note, Stunden, Status)
    """

    def __init__(self, repo):
        self.repo = repo
        self.studiengang = self.repo.load()
        if self.studiengang.semester_liste:
            self.aktuelles_semester = self.studiengang.semester_liste[0].nummer
        else:
            self.aktuelles_semester = 1

    # ---------- Semester-Navigation ----------

    def get_semester_nummern(self) -> list[int]:
        return [s.nummer for s in self.studiengang.semester_liste]

    def wechsel_semester(self, nummer: int) -> None:
        self.aktuelles_semester = nummer

    def _get_semester(self) -> Optional[Semester]:
        for s in self.studiengang.semester_liste:
            if s.nummer == self.aktuelles_semester:
                return s
        return None

    # ---------- Daten für GUI ----------

    def get_uebersicht(self) -> dict:
        sem = self._get_semester()

        if sem is None:
            return {
                "semester": None,
                "modules": [],
                "gesamt_durchschnitt": self.studiengang.gesamtdurchschnitt,
                "sem_durchschnitt": None,
                "ist_stunden": 0,
                "ziel_stunden": 0,
                "bestandene_module": 0,
                "modul_anzahl": 0,
                "ziel_durchschnitt": self.studiengang.ziel_durchschnitt,
            }

        return {
            "semester": sem,
            "modules": sem.module,
            "gesamt_durchschnitt": self.studiengang.gesamtdurchschnitt,
            "sem_durchschnitt": sem.berechne_durchschnittsnote,
            "ist_stunden": sem.berechne_ist_arbeitsaufwand,
            "ziel_stunden": sem.ziel_arbeitsaufwand_h,
            "bestandene_module": sem.zaehle_bestandene_module,
            "modul_anzahl": len(sem.module),
            "ziel_durchschnitt": self.studiengang.ziel_durchschnitt,
        }

    # ---------- Eingabe-Update ----------

    def update_modulwerte(
        self,
        modul: Modul,
        note_str: str | None,
        stunden_str: str | None,
        status_str: str | None,
    ) -> None:
        """
        Aktualisiert Note, Zeit und Status eines Moduls.

        Regeln:
        - Note muss zwischen 1.0 und 5.0 liegen
        - Note == 5.0  -> Status immer NICHT_BESTANDEN
        - Note < 5.0   -> Status:
              - wenn Status gewählt: den übernommen
              - sonst: automatisch aus Note (<=4.0 -> BESTANDEN, >4.0 -> NICHT_BESTANDEN)
        - Bei ungültiger Note wird ValueError geworfen.
        """
        today = datetime.date.today()

        # alles überschreiben, nicht aufsummieren
        modul.pruefungsleistungen.clear()
        modul.zeitinvestitionen.clear()

        # Note / Status
        if note_str:
            note_str = note_str.strip().replace(",", ".")
            try:
                note = Decimal(note_str)
            except Exception:
                raise ValueError("Die Note muss eine Zahl sein, z.B. 2,7 oder 3.")

            # --- VALIDIERUNG: nur 1.0 bis 5.0 erlaubt ---
            if note < Decimal("1.0") or note > Decimal("5.0"):
                raise ValueError("Die Note muss zwischen 1,0 und 5,0 liegen.")

            # --- STATUS-LOGIK ---
            if note == Decimal("5.0"):
                # immer nicht bestanden, egal was im Statusfeld steht
                status = Modulstatus.NICHT_BESTANDEN
            else:
                if status_str:
                    status = Modulstatus(status_str)
                else:
                    # automatische Bewertung: <=4 bestanden, >4 nicht bestanden
                    status = (
                        Modulstatus.BESTANDEN
                        if note <= Decimal("4.0")
                        else Modulstatus.NICHT_BESTANDEN
                    )

            modul.pruefungsleistungen.append(
                Pruefungsleistung(
                    art="Klausur",
                    note=note,
                    versuch=1,
                    datum=today,
                    status=status,
                )
            )

        # Zeitinvestition
        if stunden_str:
            stunden_str = stunden_str.strip()
            if stunden_str:
                try:
                    stunden = int(stunden_str)
                except Exception:
                    raise ValueError("Die Zeit (Std) muss eine ganze Zahl sein.")
                modul.zeitinvestitionen.append(
                    Zeitinvestition(
                        datum=today,
                        stunden=stunden,
                        beschreibung="GUI-Eingabe",
                    )
                )

        self.speichere()

    def speichere(self) -> None:
        self.repo.save(self.studiengang)
