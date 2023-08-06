from qtcurate.config import BASE_URL
from qtcurate.qt import Qt
import requests
import json
import os.path
from typing import Dict, List, Union
from qtcurate.exceptions import QtArgumentError, QtVocabularyError, QtConnectionError, QtRestApiError

dic_entries = "entries"
dic_name = "name"


class QtDict(Qt):
    def __init__(self, environment: str = ""):
        self.session = requests.Session()
        self.headers = {"X-API-Key": Qt.api_key}
        self.temp_dict = dict()
        self.temp_dict[dic_entries] = []
        self.temp_dict[dic_name] = None
        self.id = None
        if environment != "":
            environment = environment + "."
        self.url = f"http://{environment}{BASE_URL}dictionaries/"

    def __repr__(self):
        return str({'name': self.temp_dict[dic_name], 'entries': self.temp_dict[dic_entries]})

    def get_id(self) -> str:
        return str(self.id)


    def name(self, name: str) -> None:
        """Create a new name for dictionary"""

        if isinstance(name, str):
            self.temp_dict[dic_name] = name
        else:
            raise QtArgumentError("Argument type error: String is expected as name")

    def entries(self, entry: Dict) -> None:
        """Create dictionary data"""
        if not isinstance(entry, Dict):
            raise QtArgumentError("Argument type error: QtDict is expected as entry")
        elif len(entry) > 2 or len(entry) == 0:
            raise QtArgumentError("Argument error: QtDict must have 1 or 2 elements where keys are 'str' and "
                                  "optional 'category'."
                                  "Example {'str': 'some str', 'category': 'some category'} or just {'str':'some str'}")
        elif "str" not in entry.keys():
            raise QtArgumentError("Argument error: QtDict must have 1 or 2 elements where keys are 'str' and "
                                  "optional 'category'."
                                  "Example {'str': 'some str', 'category': 'some category'} or just {'str':'some str'}")
        elif len(set(entry.keys()).difference({"str", "category"})) != 0:
            raise QtArgumentError("Argument error: QtDict must have 1 or 2 elements where keys are 'str' and "
                                  "optional 'category'."
                                  "Example {'str': 'some str', 'category': 'some category'} or just {'str':'some str'}")
        else:
            self.temp_dict[dic_entries].append(entry)

    def clear(self) -> None:
        """Remove all temporary data"""

        self.temp_dict[dic_entries] = []
        self.temp_dict[dic_name] = None
        self.id = None

    def add_entry(self, str_key: Union[str, int, float], category: Union[str, int, float] = None) -> None:
        """Create dictionary data"""
        has_category = False
        if category is not None:
            has_category = True
        if not isinstance(str_key, (str, int, float)):
            raise QtArgumentError("Argument type error: String, integer or float are expected as key")
        elif not isinstance(category, (str, int, float)) and has_category:
            raise QtArgumentError("Argument type error: String, integer or float is expected as value")
        else:
            if has_category:
                self.temp_dict[dic_entries].append({'str': str_key, 'category': category})
            else:
                self.temp_dict[dic_entries].append({'str': str_key})

    def list(self) -> Dict:
        """List all dictionaries"""

        try:
            res = self.session.get(self.url, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")

        return res.json()

    def fetch(self, qt_id: str) -> Dict:
        """Fetch dictionary by ID"""

        if not isinstance(qt_id, str):
            raise QtArgumentError("Argument type error: String is expected as qt_id")

        try:
            res = self.session.get(f"{self.url}{qt_id}", headers=self.headers)

        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")

        self.id = res.json()["id"]
        return res.json()

    def delete(self, qt_id: str) -> bool:
        """Delete existing dictionary"""

        if not isinstance(qt_id, str):
            raise QtArgumentError("Argument type error: String is expected as qt_id")
        try:
            res = self.session.delete( f"{self.url}{qt_id}", headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")

        return res.ok

    def create(self) -> Dict:
        """Create dictionary data"""

        if self.temp_dict[dic_name] is None:
            raise QtVocabularyError("QtDict error: Please add name using name function")
        if len(self.temp_dict[dic_entries]) == 0:
            raise QtVocabularyError("QtDict error: Please add dictionary using add_entry function")
        data = {'name': self.temp_dict[dic_name], 'entries': self.temp_dict[dic_entries]}
        self.headers['Content-Type'] = 'application/json'
        try:
            res = self.session.post(self.url, headers=self.headers, data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")

        self.id = res.json()["id"]
        del self.headers['Content-Type']
        return res.json()

    def update(self, qt_id: str) -> bool:
        """Update existing dictionary"""

        if not isinstance(qt_id, str):
            raise QtArgumentError("Argument type error: String is expected as qt_id")
        if self.temp_dict[dic_name] is None:
            raise QtVocabularyError("QtDict error: Please add name using name function")
        if len(self.temp_dict[dic_entries]) == 0:
            raise QtVocabularyError("QtDict error: Please add dictionary using add_entry function")
        data = {'name': self.temp_dict[dic_name], 'entries': self.temp_dict[dic_entries]}
        try:
            res = self.session.put( f"{self.url}{qt_id}", headers=self.headers, data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")

        return res.ok

    def upload(self, file: str, name: str) -> Dict:
        """Upload dictionary data from TSV files"""

        if not isinstance(file, str):
            raise QtArgumentError("Argument type error: String is expected as file")
        if not isinstance(name, str):
            raise QtArgumentError("Argument type error: String is expected as name")
        extension = os.path.splitext(file)[1].lower()
        if extension != ".tsv":
            raise QtArgumentError("Argument type error: TSV file expected")
        if not os.path.exists(file):
            raise QtArgumentError(f"Argument error: File {file} does not exist")
        files = {
            'name': (None, name),
            'file': open(file, 'rb')
        }
        try:
            res = self.session.post(f"{self.url}upload", headers=self.headers, files=files)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")

        self.id = res.json()["id"]

        return res.json()
