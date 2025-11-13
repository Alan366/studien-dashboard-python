from abc import ABC, abstractmethod
from domain.studiengang import Studiengang


class IStudiengangRepositoryPort(ABC):

    @abstractmethod
    def load(self) -> Studiengang:
        pass

    @abstractmethod
    def save(self, studiengang: Studiengang) -> None:
        pass
