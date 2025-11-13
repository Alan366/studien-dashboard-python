from decimal import Decimal
import datetime

from domain.pruefungsleistung import Pruefungsleistung
from domain.zeitinvestition import Zeitinvestition
from domain.modulstatus import Modulstatus


class DashboardController:

    def __init__(self, repo):
        self.repo = repo
        self.studiengang = self.repo.load()
        self.aktuelles_semester = 1

    def wechsel_semester(self, nummer: int):
        self.aktuelles_semester = nummer

    def get_semester(self):
        for s in self.studiengang.semester_liste:
            if s.nummer == self.aktuelles_semester:
                return s
        return None

    def hinzufuegen_pruefungsleistung(self, modul, art, note, versuch, status):
        modul.pruefungsleistungen.append(
            Pruefungsleistung(
                art=art,
                note=Decimal(note),
                versuch=versuch,
                datum=datetime.date.today(),
                status=Modulstatus(status)
            )
        )

    def erfasse_zeit(self, modul, stunden, beschreibung):
        modul.zeitinvestitionen.append(
            Zeitinvestition(
                datum=datetime.date.today(),
                stunden=stunden,
                beschreibung=beschreibung
            )
        )

    def speichere(self):
        self.repo.save(self.studiengang)
