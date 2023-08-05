from datetime import datetime

import attr


@attr.s
class Metadata:
    url: str = attr.ib()
    title: str = attr.ib()
    description: str = attr.ib()
    capture_date: datetime = attr.ib(default=datetime.min)

    def sanitize_dir(self) -> str:
        sanitize_title = self.title.lower().replace(' ', '_').replace('|', '_').replace(':', '_')\
            .replace('/', '_').replace('"', '')
        sanitize_date = self.capture_date.strftime('%Y%m%d')

        return f'{sanitize_date}__{sanitize_title}'

    def tomanifest(self) -> dict:
        serialized = attr.asdict(self)
        serialized["capture_date"] = self.capture_date.isoformat()
        return serialized

    def tocapture(self) -> dict:
        serialized = attr.asdict(self)
        serialized["capture_date"] = self.capture_date.strftime('%d/%m/%Y')
        return serialized
