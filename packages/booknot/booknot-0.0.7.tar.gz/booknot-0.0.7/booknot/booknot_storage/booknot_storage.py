from abc import ABCMeta, abstractmethod


class BooknotStorage:
    __metaclass__ = ABCMeta

    @abstractmethod
    def exists(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def init_store(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def create_sphinx(self, project, author) -> None:
        raise NotImplementedError()

    @abstractmethod
    def is_sphinx_present(self) -> bool:
        raise NotImplementedError()
