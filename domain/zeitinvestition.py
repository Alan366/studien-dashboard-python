from dataclasses import dataclass
import datetime

@dataclass
class Zeitinvestition:
    datum: datetime.date
    stunden: int
    beschreibung: str
