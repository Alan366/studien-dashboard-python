from persistence.file_studiengang_repository import FileStudiengangRepository
from persistence.json_adapter import JsonAdapter
from controller.dashboard_controller import DashboardController
from ui.dashboard_app import DashboardApp


if __name__ == "__main__":
    repo = FileStudiengangRepository("studiengang.json", JsonAdapter())
    controller = DashboardController(repo)
    app = DashboardApp(controller)
    app.mainloop()
