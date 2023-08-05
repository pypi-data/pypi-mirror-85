from abc import ABCMeta, abstractmethod

from booknot.crawler.metadata import Metadata


class Crawler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def fetch(self, url: str) -> Metadata:
        raise NotImplementedError()
