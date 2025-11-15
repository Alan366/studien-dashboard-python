# persistence/excel_adapter.py
import pandas as pd
from collections import defaultdict


class ExcelAdapter:
    """
    Liest module.xlsx und liefert:
    { semester_nr: [modulname1, modulname2, ...] }
    Alle anderen Spalten werden ignoriert.
    """

    def read_module_list(self, path: str) -> dict[int, list[str]]:
        df = pd.read_excel(path)

        if "Semester" not in df.columns or "Modulname" not in df.columns:
            raise ValueError("Excel muss mindestens die Spalten 'Semester' und 'Modulname' enthalten.")

        mapping: dict[int, list[str]] = defaultdict(list)
        for _, row in df.iterrows():
            sem = int(row["Semester"])
            name = str(row["Modulname"]).strip()
            if not name:
                continue
            mapping[sem].append(name)

        return dict(mapping)
