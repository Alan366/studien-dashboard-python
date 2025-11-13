import tkinter as tk
from tkinter import ttk
from ui.main_view import MainView


class DashboardApp(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Studien-Dashboard")
        self.geometry("800x600")

        MainView(self, controller).pack(fill="both", expand=True)
