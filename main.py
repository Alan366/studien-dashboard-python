# main.py
from persistence.file_studiengang_repository import FileStudiengangRepository
from persistence.json_adapter import JsonAdapter
from persistence.excel_adapter import ExcelAdapter
from controller.dashboard_controller import DashboardController
from ui.dashboard_app import DashboardApp


if __name__ == "__main__":
    repo = FileStudiengangRepository(
        json_path="studiengang.json",
        json_adapter=JsonAdapter(),
        excel_path="module.xlsx",
        excel_adapter=ExcelAdapter(),
    )
    controller = DashboardController(repo)
    app = DashboardApp(controller)
    app.mainloop()
