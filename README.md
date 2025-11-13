# Studien-Dashboard (Python OOP Prototyp)

Dieses Repository enthält den fertigen Dashboard-Prototypen für den Kurs  
**Objektorientierte und funktionale Programmierung mit Python (DLBDSOOFPP01_D)**  
an der IU Internationalen Hochschule.

Der Code basiert vollständig auf der in Phase 1 und Phase 2 definierten Architektur
(UML, Domänenmodell, Repository-Pattern, Ports/Adapter, Tkinter-GUI).

---

## 🚀 Features

- OOP-Modellierung gemäß Phase 1 & 2 (Studiengang, Semester, Modul, Prüfungsleistung, Zeitinvestitionen)
- Abgeleitete Kennzahlen:
  - Durchschnittsnoten
  - Arbeitsstunden pro Semester
  - Bestanden-Progress
- Persistenz über JSON (Adapter/Repository)
- Tkinter GUI (Prototyp, kein Endprodukt)
- Modularer Clean-Architecture Aufbau (Domain → Controller → GUI)
- Vollständig dokumentierter Programmcode

---

## 📁 Projektstruktur

projekt/
│
├── domain/ # Domänenklassen
├── controller/ # DashboardController (Bindeglied GUI↔Domäne)
├── persistence/ # Repository + JSON-Adapter
├── ui/ # Tkinter GUI
│
└── main.py # Einstiegspunkt


---

## ▶️ Installation & Start

### Voraussetzungen
- Python 3.12+
- pip installiert

### Installation
```bash
pip install -r requirements.txt   # optional falls benutzt
