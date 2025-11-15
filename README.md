# Studien-Dashboard (Python OOP Prototyp)

Dieses Repository enthält den Dashboard-Prototypen für den Kurs  
**Objektorientierte und funktionale Programmierung mit Python (DLBDSOOFPP01_D)**  
an der IU Internationalen Hochschule.

Der Prototyp bildet den Studiengang **„Cyber Security Bachelor“** ab.  
Die Architektur orientiert sich an Phase 1 und Phase 2 (UML, Domänenmodell, Repository-Pattern, Ports/Adapter, Tkinter-GUI).

Getestet u. a. unter Windows 11 und macOS Tahoe 26.01.1.

---

## Features

- Objektorientiertes Modell:
  - Studiengang, Semester, Modul
  - Prüfungsleistungen, Zeitinvestitionen
- Modulnamen werden aus einer Excel-Datei (`module.xlsx`) geladen  
  (Module für Semester 1–6 des Studiengangs „Cyber Security Bachelor“)
- Pro Modul erfassbar:
  - Note
  - Zeitaufwand (Stunden)
  - Status (BESTANDEN / NICHT_BESTANDEN)
- Kennzahlen:
  - Durchschnittsnote pro Semester
  - Gesamtzeitaufwand pro Semester
  - Anzahl bestandener Module / Gesamtanzahl
- Zielgrößen im Dashboard:
  - ca. 600 Stunden Arbeitsaufwand pro Semester
  - ca. 2,5 Durchschnittsnote pro Semester
  - alle Module bestehen
- Bewertungslogik:
  - Note muss zwischen 1,0 und 5,0 liegen
  - Note = 5,0 → immer NICHT_BESTANDEN
  - ohne manuellen Status:
    - Note ≤ 4,0 → BESTANDEN
    - Note > 4,0 → NICHT_BESTANDEN
- Persistenz über JSON-Repository
- Tkinter-GUI mit:
  - Tabelle der Module
  - Modul-Auswahl per Tabelle oder Dropdown
  - Eingabefeldern für Note, Zeit, Status
  - Ziel/Ist-Anzeige im Kopfbereich

---

## Projektstruktur

```text

studien-dashboard-python/
│
├── domain/                  # Domänenklassen (Studiengang, Semester, Modul, ...)
├── controller/              # DashboardController (Logik zwischen GUI und Domain)
├── persistence/             # Repository + JSON-Adapter
├── ui/                      # Tkinter-GUI (DashboardApp, MainView)
│
├── module.xlsx              # Excel mit Modulnamen (wird eingelesen)
├── create_module_excel.py   # Skript zum Erzeugen von module.xlsx
├── requirements.txt         # Python-Abhängigkeiten (pandas, openpyxl, ...)
├── main.py                  # Einstiegspunkt: startet die GUI
└── README.md                # dieses Dokument

---
## Projektstruktur

## Installation und Start:


Voraussetzungen

- Python 3.12 oder höher
- pip installiert
- optional: Visual Studio Code mit Python-Erweiterung

bash:
- python --version
- python -m pip --version

Excel-Datei mit Modulen erzeugen (falls noch nicht vorhande
 - python create_module_excel.py ausführen

Dashboard starten:

- python main.py


