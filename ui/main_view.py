import tkinter as tk
from tkinter import ttk


class MainView(tk.Frame):
    """Sehr reduzierter UI-Prototyp – nur das Nötigste."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Dashboard – Prototyp", font=("Arial", 18)).pack(pady=10)

        # Dropdown Semester
        sem_numbers = [s.nummer for s in controller.studiengang.semester_liste]
        self.sem_var = tk.IntVar(value=sem_numbers[0] if sem_numbers else 1)
        ttk.Combobox(self, values=sem_numbers, textvariable=self.sem_var).pack()

        tk.Button(self, text="Semester wechseln",
                  command=self.on_semester_change).pack(pady=10)

        self.output = tk.Text(self, height=20)
        self.output.pack(fill="both", expand=True)
        self.update_output()

    def on_semester_change(self):
        self.controller.wechsel_semester(self.sem_var.get())
        self.update_output()

    def update_output(self):
        sem = self.controller.get_semester()
        self.output.delete("1.0", tk.END)

        if not sem:
            self.output.insert(tk.END, "Keine Semester angelegt.")
            return

        self.output.insert(tk.END, f"Semester {sem.nummer}\n")
        self.output.insert(tk.END, f"Arbeitsaufwand: {sem.berechne_ist_arbeitsaufwand}h / {sem.ziel_arbeitsaufwand_h}h\n")
        self.output.insert(tk.END, f"Durchschnittsnote: {sem.berechne_durchschnittsnote}\n")
        self.output.insert(tk.END, f"Bestandene Module: {sem.zaehle_bestandene_module}\n\n")

        self.output.insert(tk.END, "Module:\n")
        for m in sem.module:
            self.output.insert(tk.END, f"- {m.titel}: Status={m.aktueller_status.value}, Zeit={m.gesamt_zeitinvest}h\n")
