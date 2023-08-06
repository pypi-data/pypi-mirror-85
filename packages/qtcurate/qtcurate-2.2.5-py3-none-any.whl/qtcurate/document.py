from qtcurate.qt import Qt
from smart_open import open
from qtcurate.exceptions import QtArgumentError
from qtcurate.connect import connect


class Document:
    def __init__(self):
        self.headers = {"X-API-Key": Qt.api_key}
        self.url = Qt.url
        self.id = None

    def __repr__(self):
        return f"{self.id}"

    def set_id(self, uuid: str) -> None:
        """Set document id"""

        if isinstance(uuid, str):
            self.id = uuid
        else:
            raise QtArgumentError("Argument type error: String is expected as uuid")

    def get_id(self) -> str:
        """Get document id"""

        return self.id

    def create(self, file: str) -> str:
        """Upload files for data mining"""

        if not isinstance(file, str):
            raise QtArgumentError("Argument type error: String is expected as file path")
        files = {'file': open(file, 'rb')}
        res = connect("post", f"{self.url}search/file", self.headers, "files", files)

        return res.json()["uuid"]

