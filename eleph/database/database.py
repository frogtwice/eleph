from abc import ABC, abstractmethod
from dataclasses import dataclass


class Database(ABC):
    @abstractmethod
    def select[T: Row](self, row: T) -> T:
        ...

    @abstractmethod
    def insert[T: Row](self, row: T):
        ...

    @abstractmethod
    def upsert[T: Row](self, row: T):
        ...


@dataclass
class Row:
    table_name: str
