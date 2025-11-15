import tkinter as tk
from tkinter import ttk, messagebox


class MainView(tk.Frame):
    """
    GUI:
    - oben: Studiengang + Gesamtdurchschnitt + Ziele (Ziel + aktuell)
    - Mitte: Tabelle mit Modulen
    - darunter: Modul-Auswahl + Eingabe Note/Zeit/Status
    - unten: Kacheln mit IST-Werten (Zeit, Durchschnitt, Fortschritt)
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.selected_modul_name = None
        self.current_modules = []

        # ---------- TOP ----------
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", padx=20, pady=(15, 5))

        left = tk.Frame(top, bg="white")
        left.pack(side="left")

        # Studiengang-Name
        self.label_stg = tk.Label(
            left,
            text=self.controller.studiengang.name,
            font=("Arial", 18, "bold"),
            bg="white",
        )
        self.label_stg.pack(anchor="w")

        # Gesamtdurchschnitt (wird in _refresh gesetzt)
        self.label_gesamt = tk.Label(
            left,
            text="Gesamtdurchschnittsnote: –",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        self.label_gesamt.pack(anchor="w", pady=(2, 5))

        # --- ZIELE: dynamische Labels (werden in _refresh gesetzt) ---
        goals = tk.Frame(left, bg="white")
        goals.pack(anchor="w", pady=(0, 5))

        self.lbl_goal_zeit = tk.Label(
            goals,
            text="",
            bg="white",
            fg="gray20",
            font=("Arial", 9),
        )
        self.lbl_goal_zeit.pack(anchor="w")

        self.lbl_goal_note = tk.Label(
            goals,
            text="",
            bg="white",
            fg="gray20",
            font=("Arial", 9),
        )
        self.lbl_goal_note.pack(anchor="w")

        self.lbl_goal_fortschritt = tk.Label(
            goals,
            text="",
            bg="white",
            fg="gray20",
            font=("Arial", 9),
        )
        self.lbl_goal_fortschritt.pack(anchor="w")

        # Semester-Auswahl rechts
        right = tk.Frame(top, bg="white")
        right.pack(side="right")

        tk.Label(right, text="Semester", bg="white", font=("Arial", 10)).pack(
            side="left", padx=5
        )

        self.sem_var = tk.IntVar()
        sem_list = self.controller.get_semester_nummern()
        self.sem_var.set(sem_list[0] if sem_list else 1)

        self.sem_combo = ttk.Combobox(
            right,
            values=sem_list,
            textvariable=self.sem_var,
            width=5,
            state="readonly",
        )
        self.sem_combo.pack(side="left")
        self.sem_combo.bind("<<ComboboxSelected>>", self._on_semester_change)

        # ---------- TABELLE ----------
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="x", padx=20, pady=(5, 0))

        cols = ("modul", "note", "zeit", "status")
        self.tree = ttk.Treeview(
            table_frame,
            columns=cols,
            show="headings",
            height=6,  # bewusst kleiner, damit unten Platz bleibt
            style="Custom.Treeview",
        )
        self.tree.heading("modul", text="Modulname", anchor="w")
        self.tree.heading("note", text="Note")
        self.tree.heading("zeit", text="Zeitinvestition")
        self.tree.heading("status", text="Status")

        self.tree.column("modul", anchor="w", width=350)
        self.tree.column("note", anchor="center", width=80)
        self.tree.column("zeit", anchor="center", width=120)
        self.tree.column("status", anchor="center", width=140)

        self.tree.pack(fill="x")
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # ---------- EINGABE-FORM ----------
        form_outer = tk.Frame(self, bg="white")
        form_outer.pack(fill="x", padx=20, pady=(10, 5))

        form = tk.Frame(form_outer, bg="white")
        form.pack(anchor="w")

        # Modul-Auswahl (Dropdown)
        tk.Label(form, text="Modul:", bg="white").grid(row=0, column=0, sticky="e")
        self.modul_var = tk.StringVar()
        self.modul_combo = ttk.Combobox(
            form,
            textvariable=self.modul_var,
            values=[],
            width=40,
            state="readonly",
        )
        self.modul_combo.grid(row=0, column=1, columnspan=3, sticky="w", padx=(5, 20))
        self.modul_combo.bind("<<ComboboxSelected>>", self._on_modul_combo_change)

        self.label_selected = tk.Label(
            form,
            text="Kein Modul ausgewählt",
            bg="white",
            font=("Arial", 9, "italic"),
        )
        self.label_selected.grid(row=0, column=4, columnspan=3, sticky="w")

        # Zeile 2: Note / Zeit / Status / Button
        tk.Label(form, text="Note:", bg="white").grid(
            row=1, column=0, sticky="e", pady=(8, 0)
        )
        self.entry_note = tk.Entry(
            form, width=10, bg="white", fg="black", relief="solid", bd=1
        )
        self.entry_note.grid(row=1, column=1, sticky="w", padx=(5, 20), pady=(8, 0))

        tk.Label(form, text="Zeit (Std):", bg="white").grid(
            row=1, column=2, sticky="e", pady=(8, 0)
        )
        self.entry_stunden = tk.Entry(
            form, width=10, bg="white", fg="black", relief="solid", bd=1
        )
        self.entry_stunden.grid(row=1, column=3, sticky="w", padx=(5, 20), pady=(8, 0))

        tk.Label(form, text="Status:", bg="white").grid(
            row=1, column=4, sticky="e", pady=(8, 0)
        )
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(
            form,
            textvariable=self.status_var,
            values=["", "BESTANDEN", "NICHT_BESTANDEN"],
            width=18,
            state="readonly",
        )
        self.status_combo.grid(
            row=1, column=5, sticky="w", padx=(5, 20), pady=(8, 0)
        )

        self.btn_save = tk.Button(
            form,
            text="Werte speichern",
            command=self._on_save_clicked,
            bg="white",
            relief="solid",
            bd=1,
            padx=10,
            pady=3,
        )
        self.btn_save.grid(row=1, column=6, sticky="w", pady=(8, 0))

        hint = tk.Label(
            form_outer,
            text="Hinweis: Wenn Status leer bleibt, wird er aus der Note berechnet (<=4 bestanden).",
            bg="white",
            fg="gray",
            font=("Arial", 9),
        )
        hint.pack(anchor="w", pady=(5, 0))

        # ---------- KPI-BEREICH (IST-WERTE) ----------
        kpi_frame = tk.Frame(self, bg="white")
        kpi_frame.pack(fill="x", padx=20, pady=(10, 15))

        # Karte 1: Zeitaufwand (Ist)
        self.card_zeit = self._build_card(kpi_frame, "Gesamtzeitaufwand (Ist)")
        self.card_zeit.pack(side="left", expand=True, fill="x", padx=5)

        self.lbl_zeit_ist = tk.Label(self.card_zeit, text="", bg="white", anchor="w")
        self.lbl_zeit_ist.pack(anchor="w")
        self.pb_zeit = ttk.Progressbar(self.card_zeit, mode="determinate")
        self.pb_zeit.pack(fill="x", pady=(4, 0))

        # Karte 2: Durchschnittsnote (Ist)
        self.card_note = self._build_card(kpi_frame, "Durchschnittsnote (Ist)")
        self.card_note.pack(side="left", expand=True, fill="x", padx=5)

        self.lbl_note_ist = tk.Label(
            self.card_note, text="–", font=("Arial", 18, "bold"), bg="white"
        )
        self.lbl_note_ist.pack()

        # Karte 3: Fortschrittsanzeige (Ist)
        self.card_fortschritt = self._build_card(kpi_frame, "Fortschrittsanzeige (Ist)")
        self.card_fortschritt.pack(side="left", expand=True, fill="x", padx=5)

        self.lbl_fortschritt_ist = tk.Label(
            self.card_fortschritt, text="", bg="white", anchor="w"
        )
        self.lbl_fortschritt_ist.pack(anchor="w")
        self.pb_fortschritt = ttk.Progressbar(
            self.card_fortschritt, mode="determinate"
        )
        self.pb_fortschritt.pack(fill="x", pady=(4, 0))

        # initiale Anzeige
        self._refresh()

    # ---------- Hilfsfunktionen ----------

    def _build_card(self, parent, title):
        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        tk.Label(
            frame, text=title, font=("Arial", 10, "bold"), bg="white"
        ).pack(anchor="w", padx=10, pady=5)
        inner = tk.Frame(frame, bg="white")
        inner.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        return inner

    def _fmt(self, value):
        if value is None:
            return "–"
        return str(round(float(value), 2)).replace(".", ",")

    # ---------- Events ----------

    def _on_semester_change(self, _event=None):
        self.controller.wechsel_semester(self.sem_var.get())
        self.selected_modul_name = None
        self.modul_var.set("")
        self.label_selected.config(text="Kein Modul ausgewählt")
        self.entry_note.delete(0, tk.END)
        self.entry_stunden.delete(0, tk.END)
        self.status_var.set("")
        self._refresh()

    def _on_tree_select(self, _event=None):
        selection = self.tree.selection()
        if not selection:
            return
        item_id = selection[0]
        values = self.tree.item(item_id, "values")
        modulname = values[0]
        self._select_modul(modulname)

    def _on_modul_combo_change(self, _event=None):
        modulname = self.modul_var.get().strip()
        if modulname:
            self._select_modul(modulname)

    def _select_modul(self, modulname: str):
        self.selected_modul_name = modulname
        self.modul_var.set(modulname)
        self.label_selected.config(text=f"Ausgewähltes Modul: {modulname}")

        modul = next((m for m in self.current_modules if m.titel == modulname), None)
        if not modul:
            return

        # Felder füllen
        self.entry_note.delete(0, tk.END)
        if modul.aktuelle_note is not None:
            self.entry_note.insert(0, self._fmt(modul.aktuelle_note))

        self.entry_stunden.delete(0, tk.END)
        if modul.gesamt_zeitinvest:
            self.entry_stunden.insert(0, str(modul.gesamt_zeitinvest))

        status = modul.aktueller_status
        if status is not None:
            self.status_var.set(status.value)
        else:
            self.status_var.set("")

    def _on_save_clicked(self):
        modulname = (self.modul_var.get() or "").strip()
        if not modulname:
            self.label_selected.config(
                text="Bitte zuerst ein Modul im Dropdown oder in der Tabelle auswählen."
            )
            return

        modul = next((m for m in self.current_modules if m.titel == modulname), None)
        if not modul:
            self.label_selected.config(text="Modul nicht gefunden.")
            return

        note_str = self.entry_note.get().strip()
        stunden_str = self.entry_stunden.get().strip()
        status_str = self.status_var.get().strip()
        if status_str == "":
            status_str = None

        try:
            self.controller.update_modulwerte(
                modul,
                note_str or None,
                stunden_str or None,
                status_str,
            )
        except ValueError as e:
            # Eingabefehler (z.B. Note > 5) anzeigen
            messagebox.showerror("Eingabefehler", str(e))
            return

        self._refresh()
        self.label_selected.config(text=f"Werte gespeichert für: {modulname}")

    # ---------- Refresh ----------

    def _refresh(self):
        data = self.controller.get_uebersicht()
        self.current_modules = data["modules"]

        # Top: Gesamtdurchschnitt über alle Semester
        self.label_gesamt.config(
            text=f"Gesamtdurchschnittsnote: {self._fmt(data['gesamt_durchschnitt'])}"
        )

        # --- Ziele dynamisch setzen (Ziel + aktuell) ---
        ist_stunden = data["ist_stunden"] or 0
        ziel_stunden = data["ziel_stunden"] or 0
        self.lbl_goal_zeit.config(
            text=(
                f"Gesamtzeitaufwand pro Semester: "
                f"Ziel ca. {ziel_stunden} Std / aktuell: {ist_stunden} Std"
            )
        )

        sem_note = data["sem_durchschnitt"]
        ziel_note = data["ziel_durchschnitt"]
        sem_note_str = self._fmt(sem_note)
        ziel_note_str = (
            str(ziel_note).replace(".", ",") if ziel_note is not None else "–"
        )
        self.lbl_goal_note.config(
            text=(
                f"Durchschnittsnote pro Semester: "
                f"Ziel ca. {ziel_note_str} / aktuell: {sem_note_str}"
            )
        )

        best = data["bestandene_module"]
        total = data["modul_anzahl"]
        self.lbl_goal_fortschritt.config(
            text=(
                "Fortschritt: Ziel alle Module bestehen"
                f" / aktuell: {best} von {total} Modulen"
            )
        )

        # Modul-Dropdown füllen
        modul_namen = [m.titel for m in self.current_modules]
        self.modul_combo["values"] = modul_namen
        if self.selected_modul_name not in modul_namen:
            self.modul_var.set("")
            self.selected_modul_name = None
            self.label_selected.config(text="Kein Modul ausgewählt")

        # Tabelle leeren
        for r in self.tree.get_children():
            self.tree.delete(r)

        # Tabelle füllen (Status leer, wenn None)
        for m in self.current_modules:
            status = m.aktueller_status
            status_text = status.value if status is not None else ""

            self.tree.insert(
                "",
                "end",
                values=(
                    m.titel,
                    self._fmt(m.aktuelle_note),
                    f"{m.gesamt_zeitinvest} Std",
                    status_text,
                ),
            )

        # KPI 1: Zeit (Ist)
        self.lbl_zeit_ist.config(text=f"Ist: {ist_stunden} von {ziel_stunden} Stunden")
        self.pb_zeit.config(maximum=ziel_stunden if ziel_stunden else 1, value=ist_stunden)

        # KPI 2: Durchschnitt (Ist)
        self.lbl_note_ist.config(text=sem_note_str)

        # KPI 3: Fortschritt (Ist)
        self.lbl_fortschritt_ist.config(
            text=f"Ist: {best} von {total} Modulen bestanden"
        )
        self.pb_fortschritt.config(maximum=total if total else 1, value=best)
