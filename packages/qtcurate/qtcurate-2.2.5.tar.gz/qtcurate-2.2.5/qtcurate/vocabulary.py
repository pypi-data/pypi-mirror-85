from __future__ import annotations
from qtcurate.qt import Qt
import json
import os.path
from typing import Dict, Union, List
from qtcurate.exceptions import QtArgumentError, QtVocabularyError
from qtcurate.connect import connect

vocabulary_entries = "entries"
vocabulary_name = "name"


class Vocabulary(Qt):
    def __init__(self):
        self.headers = {"X-API-Key": Qt.api_key}
        self.temp_vocabulary = dict()
        self.temp_vocabulary[vocabulary_entries] = []
        self.temp_vocabulary[vocabulary_name] = None
        self.id = None
        self.input_stream = None
        self.url = f"{Qt.url}dictionaries/"

    def __repr__(self):
        return str({'id': self.id, 'name': self.temp_vocabulary[vocabulary_name],
                    'entries': self.temp_vocabulary[vocabulary_entries]})

    def get_id(self) -> str:
        """Get vocabulary id"""

        return str(self.id)

    def set_id(self, voc_id: str) -> Vocabulary:
        """Set vocabulary id"""

        if isinstance(voc_id, str):
            self.id = voc_id
        else:
            raise QtArgumentError("Argument type error: String is expected as id")
        return self

    def name(self, voc_name: str) -> Vocabulary:
        """Create a new name for vocabulary"""
        
        if isinstance(voc_name, str):
            self.temp_vocabulary[vocabulary_name] = voc_name
        else:
            raise QtArgumentError("Argument type error: String is expected as name")
        return self

    def get_name(self) -> str:
        """Get vocabulary name"""

        return self.temp_vocabulary[vocabulary_name]

    def entries(self, entry: Dict) -> Vocabulary:
        """Create vocabulary data"""
        
        if not isinstance(entry, Dict):
            raise QtArgumentError("Argument type error: Dictionary is expected as entry")
        elif len(entry) > 2 or len(entry) == 0:
            raise QtArgumentError("Argument error: Vocabulary must have 1 or 2 elements where keys are 'str' and "
                                  "optional 'category'."
                                  "Example {'str': 'some str', 'category': 'some category'} or just {'str':'some str'}")
        elif "str" not in entry.keys():
            raise QtArgumentError("Argument error: Vocabulary must have 1 or 2 elements where keys are 'str' and "
                                  "optional 'category'."
                                  "Example {'str': 'some str', 'category': 'some category'} or just {'str':'some str'}")
        elif len(set(entry.keys()).difference({"str", "category"})) != 0:
            raise QtArgumentError("Argument error: Vocabulary must have 1 or 2 elements where keys are 'str' and "
                                  "optional 'category'."
                                  "Example {'str': 'some str', 'category': 'some category'} or just {'str':'some str'}")
        else:
            self.temp_vocabulary[vocabulary_entries].append(entry)
        return self

    def clear(self) -> None:
        """Remove all temporary data"""

        self.temp_vocabulary[vocabulary_entries] = []
        self.temp_vocabulary[vocabulary_name] = None
        self.id = None
        self.input_stream = None

    def add_entry(self, str_key: Union[str, int, float], category: Union[str, int, float] = None) -> Vocabulary:
        """Create vocabulary data"""
        
        has_category = False
        if category is not None:
            has_category = True
        if not isinstance(str_key, (str, int, float)):
            raise QtArgumentError("Argument type error: String, integer or float are expected as key")
        elif not isinstance(category, (str, int, float)) and has_category:
            raise QtArgumentError("Argument type error: String, integer or float is expected as value")
        else:
            if has_category:
                self.temp_vocabulary[vocabulary_entries].append({'str': str_key, 'category': category})
            else:
                self.temp_vocabulary[vocabulary_entries].append({'str': str_key})
        return self

    def get_entries(self) -> List:
        """Get entries"""

        return self.temp_vocabulary[vocabulary_entries]

    def read(self) -> Dict:
        """List all vocabularies"""

        res = connect("get", self.url, self.headers)
        return res.json()

    def fetch(self, vocabulary_id: str) -> Vocabulary:
        """Fetch vocabulary by ID"""

        if not isinstance(vocabulary_id, str):
            raise QtArgumentError("Argument type error: String is expected as qt_id")

        res = connect("get", f"{self.url}{vocabulary_id}", self.headers)
        result = res.json()
        self.temp_vocabulary[vocabulary_name] = result[vocabulary_name]
        self.id = result['id']
        self.temp_vocabulary[vocabulary_entries] = result[vocabulary_entries]
        return self

    def delete(self, vocabulary_id: str) -> bool:
        """Delete existing vocabulary"""

        if not isinstance(vocabulary_id, str):
            raise QtArgumentError("Argument type error: String is expected as qt_id")
        res = connect("delete", f"{self.url}{vocabulary_id}", self.headers)

        return res.ok

    def source(self, file: str) -> Vocabulary:
        """Set source"""

        if not isinstance(file, str):
            raise QtArgumentError("Argument type error: String is expected as file")
        extension = os.path.splitext(file)[1].lower()
        if extension != ".tsv":
            raise QtArgumentError("Argument type error: TSV file expected")
        if not os.path.exists(file):
            raise QtArgumentError(f"Argument error: File {file} does not exist")
        self.input_stream = file
        return self

    def create(self) -> Vocabulary:
        """Create vocabulary data"""

        if self.temp_vocabulary[vocabulary_name] is None:
            raise QtVocabularyError("Vocab error: Please add name using name function")

        if self.input_stream is None:
            self.headers['Content-Type'] = 'application/json'
            if not self.temp_vocabulary[vocabulary_entries]:
                raise QtVocabularyError("Vocabulary error: Please add vocabulary using add_entry function")
            data = {'name': self.temp_vocabulary[vocabulary_name], 'entries': self.temp_vocabulary[vocabulary_entries]}
            res = connect("post", self.url, self.headers, "data", json.dumps(data))
            self.id = res.json()["id"]
            return self
        else:
            files = {
                'name': (None, self.temp_vocabulary[vocabulary_name]),
                'file': open(self.input_stream, 'rb')
            }
            res = connect("post", f"{self.url}upload", self.headers, "files", files)
            result = res.json()
            self.id = result["id"]
            self.temp_vocabulary[vocabulary_entries] = result[vocabulary_entries]
            return self

    def update(self, qt_id: str) -> Vocabulary:
        """Update existing vocabulary"""
        
        self.headers['Content-Type'] = 'application/json'
        if not isinstance(qt_id, str):
            raise QtArgumentError("Argument type error: String is expected as qt_id")
        if self.temp_vocabulary[vocabulary_name] is None:
            raise QtVocabularyError("Vocabulary error: Please add name using name function")
        if len(self.temp_vocabulary[vocabulary_entries]) == 0:
            raise QtVocabularyError("Vocabulary error: Please add vocabulary using add_entry function")
        data = {'name': self.temp_vocabulary[vocabulary_name], 'entries': self.temp_vocabulary[vocabulary_entries]}
        res = connect("put", f"{self.url}{qt_id}", self.headers, "data", json.dumps(data))
        self.temp_vocabulary[vocabulary_entries] = res.json()[vocabulary_entries]
        del self.headers['Content-Type']
        return self
