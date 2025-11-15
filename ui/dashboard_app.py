# ui/dashboard_app.py
import tkinter as tk
from tkinter import ttk

from ui.main_view import MainView


class DashboardApp(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        self.title("Studien-Dashboard")
        self.geometry("1050x700")
        self.configure(bg="white")

        # --- Style auf hell setzen ---
        style = ttk.Style(self)

        # neutrales, gut kontrollierbares Theme
        try:
            style.theme_use("clam")
        except tk.TclError:
            # falls clam nicht da ist, nimm Standard
            pass

        # Treeview (Tabelle)
        style.configure(
            "Custom.Treeview",
            background="white",
            foreground="black",
            fieldbackground="white",
            rowheight=24,
            borderwidth=0,
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "#E5E7FF")],
            foreground=[("selected", "#111827")],
        )

        style.configure(
            "Custom.Treeview.Heading",
            background="#F9FAFB",
            foreground="#111827",
            font=("Arial", 10, "bold"),
        )

        # Labels / Frames hell
        style.configure("TLabel", background="white")
        style.configure("TFrame", background="white")

        # Combobox etwas heller
        style.configure("TCombobox", fieldbackground="white")

        # App-Inhalt
        root_frame = tk.Frame(self, bg="white")
        root_frame.pack(fill="both", expand=True)

        MainView(root_frame, controller).pack(fill="both", expand=True)
