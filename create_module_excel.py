# create_module_excel.py
import pandas as pd

def main():
    rows = [
        # Semester, Modulname, Note, Stunden, Status
        # Semester 1
        (1, "Betriebssystem und Verteile", 3.0, 40, "BESTANDEN"),
        (1, "Math Grundlage 1", 2.7, 30, "BESTANDEN"),
        (1, "IT-Sicherheit", 2.0, 20, "BESTANDEN"),
        (1, "Python", 2.0, 35, "BESTANDEN"),
        (1, "OOP python", 2.0, 40, "BESTANDEN"),
        (1, "Math Grundlage 2", 5.0, 50, "NICHT_BESTANDEN"),
        # Semester 2
        (2, "Einführung in die Netzwerkforensik", None, None, None),
        (2, "Statistik - Wahrscheinlichkeit und deskriptive Statistik", None, None, None),
        (2, "Requirements Engineering", None, None, None),
        (2, "Projekt: Agiles Projektmanagement", None, None, None),
        (2, "Grundzüge des System-Pentestings", None, None, None),
        # Semester 3
        (3, "Social Engineering und Insider Threats", None, None, None),
        (3, "Technische und betriebliche IT-Sicherheitskonzeptionen", None, None, None),
        (3, "Projekt: Social Engineering", None, None, None),
        (3, "Theoretische Informatik und Mathematische Logik", None, None, None),
        (3, "DevSecOps und gängige Software-Schwachstellen", None, None, None),
        (3, "Praktikum: Informatik", None, None, None),
        # Semester 4
        (4, "Kryptografische Verfahren", None, None, None),
        (4, "Host- und Softwareforensik", None, None, None),
        (4, "Seminar: Aktuelle Themen in Computer Science", None, None, None),
        (4, "Projekt: Einsatz und Konfiguration von SIEM-Systemen", None, None, None),
        (4, "Praktikum: Informatik", None, None, None),
        # Semester 5
        (5, "Threat Modeling", None, None, None),
        (5, "Standards der Informationssicherheit", None, None, None),
        (5, "Projekt: Threat Modeling", None, None, None),
        (5, "Praktikum: Informatik", None, None, None),
        # Semester 6
        (6, "Bachelorarbeit", None, None, None),
        (6, "Projekt: Allgemeine Programmierung mit C/C++", None, None, None),
        (6, "Praktikum: Informatik", None, None, None),
    ]

    df = pd.DataFrame(rows, columns=["Semester", "Modulname", "Note", "Stunden", "Status"])
    df.to_excel("module.xlsx", index=False, sheet_name="Module")
    print("module.xlsx erstellt.")

if __name__ == "__main__":
    main()
