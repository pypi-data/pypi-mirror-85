from abc import ABC, abstractmethod


class BaseLocation(ABC):
    """Базовый абстрактный клас местоположения."""

    @abstractmethod
    def encode(self) -> bytes:
        pass

    def __len__(self) -> int:
        return len(self.encode())
