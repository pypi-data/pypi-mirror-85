from __future__ import annotations
from qtcurate.document import Document
from qtcurate.extractor import Extractor, Mode, ChunkMode, SearchMode, AnalyzeMode
from qtcurate.connect import connect
from time import sleep
import re
import json
from typing import Dict, List
from qtcurate.qt import Qt
from qtcurate.exceptions import QtArgumentError, QtModelError


tag_files = "files"
chunk = "chunk"
num_workers = "numWorkers"
description = "title"
vocab_id = "vocabId"
vocab_value_type = "vocabValueType"
validator = "phraseMatchingPattern"
phrase_groups = "phraseMatchingGroups"
exclude_utt = "excludeUttWithoutEntities"
search_vocabulary = "searchDictionaries"
between_values = "skipPatternBetweenValues"
search_mod = "searchMode"
analyze_strategy = "analyzeStrategy"
stop_word_list = "stopwordList"
synonym_l = "synonymList"
data_type = "dataType"
language = "language"


class Model:
    def __init__(self):
        self.headers = {"X-API-Key": Qt.api_key}
        self.temp_dictionary = dict()
        self.temp_dictionary[description] = None
        self.temp_dictionary[exclude_utt] = True
        self.temp_dictionary[num_workers] = 8
        self.temp_dictionary[chunk] = ChunkMode.PAGE.value
        self.temp_dictionary[search_vocabulary] = []
        self.index = None
        self.uuid = None
        self.id = None
        self.url = Qt.url

    def __repr__(self):
        return f"{self.id}, {self.temp_dictionary}"

    def get_id(self) -> str:
        """Get model id"""

        return str(self.id)

    def set_id(self, model_id: str) -> Model:
        """Set model id"""

        if isinstance(model_id, str):
            self.id = model_id
        else:
            raise QtArgumentError("Argument type error: String is expected as model_id")
        return self

    def set_chunk(self, value: ChunkMode) -> Model:
        """Set chunk mode"""

        if isinstance(value, ChunkMode):
            self.temp_dictionary[chunk] = value.value
        else:
            raise QtArgumentError("Argument type error: ChunkMode is expected as value")
        return self

    def get_uuid(self) -> str:
        """Get uuid"""

        return str(self.uuid)

    def set_description(self, title: str) -> Model:
        """Create title for model"""

        if isinstance(title, str):
            self.temp_dictionary[description] = title
        else:
            raise QtArgumentError("Argument type error: String is expected as description")
        return self

    def exclude_utt_without_entities(self, value: bool) -> Model:
        """Set exclude utt for mining data, this is optional parameter"""

        if isinstance(value, bool):
            self.temp_dictionary[exclude_utt] = value
        else:
            raise QtArgumentError("Argument type error: Boolean is expected as exclude utt without entities")
        return self

    def set_workers(self, value: int) -> Model:
        """Set workers"""

        if isinstance(value, int):
            self.temp_dictionary[num_workers] = value
        else:
            raise QtArgumentError("Argument type error: Integer is expected as num_workers")
        return self

    def with_documents(self, list_of_files: List) -> Model:
        """Create a list of existing files"""

        if isinstance(list_of_files, list):
            self.temp_dictionary[tag_files] = list_of_files
        else:
            raise QtArgumentError("Argument type error: Expected list of file IDs")
        return self

    def add_extractor(self, extractor: Extractor) -> Model:
        """Prepare dictionary for searching"""

        vocab_dict = dict()
        if extractor.get_vocab_id() is not None:
            vocab_dict[vocab_id] = extractor.get_vocab_id()
        if extractor.get_vocab_value_type() is not None:
            vocab_dict[vocab_value_type] = extractor.get_vocab_value_type()
        if extractor.get_type() is not None:
            vocab_dict[data_type] = extractor.get_type().value
        if extractor.get_mode() == Mode.SIMPLE:
            vocab_dict[search_mod] = SearchMode.ORDERED_SPAN.value
            vocab_dict[analyze_strategy] = AnalyzeMode.SIMPLE.value
        elif extractor.get_mode() == Mode.UNORDERED:
            vocab_dict[search_mod] = SearchMode.SPAN.value
            vocab_dict[analyze_strategy] = AnalyzeMode.SIMPLE.value
        elif extractor.get_mode() == Mode.STEM:
            vocab_dict[search_mod] = SearchMode.ORDERED_SPAN.value
            vocab_dict[analyze_strategy] = AnalyzeMode.STEM.value
        elif extractor.get_mode() == Mode.UNORDERED_STEM:
            vocab_dict[search_mod] = SearchMode.SPAN.value
            vocab_dict[analyze_strategy] = AnalyzeMode.STEM.value
        elif extractor.get_mode() == Mode.FUZZY_UNORDERED_STEM:
            vocab_dict[search_mod] = SearchMode.FUZZY_SPAN.value
            vocab_dict[analyze_strategy] = AnalyzeMode.STEM.value
        if extractor.get_stop_word_list() is not None:
            vocab_dict[stop_word_list] = extractor.get_stop_word_list()
        if extractor.get_synonym_list() is not None:
            vocab_dict[synonym_l] = extractor.get_synonym_list()
        if extractor.get_validator() is not None:
            try:
                re.compile(extractor.get_validator())
                ok = True
            except re.error:
                ok = False
            if ok is False:
                raise QtArgumentError("Argument type error: Please write valid regular expression for validator.")
            else:
                vocab_dict[validator] = extractor.get_validator()
                vocab_dict[vocab_value_type] = extractor.get_vocab_value_type()
        self.temp_dictionary[search_vocabulary].append(vocab_dict)
        return self

    def get_extractor(self, dictionary: Dict) -> Model:
        """Get extractor"""

        if search_vocabulary in dictionary:
            for i in dictionary[search_vocabulary]:
                self.temp_dictionary[search_vocabulary].append(i)
        return self

    def clear(self) -> None:
        """Remove all temporary data"""

        self.temp_dictionary.pop(tag_files, None)
        self.temp_dictionary.pop(description, None)
        self.temp_dictionary[exclude_utt] = True
        self.temp_dictionary[num_workers] = 4
        self.temp_dictionary.pop(search_vocabulary, None)
        self.index = None

    def create(self) -> Model:
        """Creating a new model"""

        self.headers["Content-Type"] = "application/json"
        data = {}
        if not self.temp_dictionary[search_vocabulary]:
            raise QtModelError("Model error: Please add parameters using add_extractor function")
        if tag_files in self.temp_dictionary and search_vocabulary in self.temp_dictionary:
            data[tag_files] = self.temp_dictionary[tag_files]
        data[exclude_utt] = self.temp_dictionary[exclude_utt]
        data[num_workers] = self.temp_dictionary[num_workers]
        data[chunk] = self.temp_dictionary[chunk]
        if search_vocabulary in self.temp_dictionary:
            data[search_vocabulary] = self.temp_dictionary[search_vocabulary]
        if description in self.temp_dictionary:
            data[description] = self.temp_dictionary[description]
        res = connect("post", f"{self.url}search/new", self.headers, "data", json.dumps(data))
        self.id = res.json()['id']
        del self.headers['Content-Type']
        return self

    def set_returned_data(self, result: Dict) -> None:
        """Set returned data from server"""

        self.temp_dictionary[description] = result[description]
        self.temp_dictionary[exclude_utt] = result[exclude_utt]
        self.temp_dictionary[search_vocabulary] = result[search_vocabulary]
        self.temp_dictionary[tag_files] = result[tag_files]
        self.temp_dictionary[chunk] = result[chunk]
        self.temp_dictionary[num_workers] = result[num_workers]

    def fetch(self, model_id: str) -> Model:
        """ Fetch model where model_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(model_id, str):
            raise QtArgumentError("Argument type error: String is expected as model_id")
        res = connect("get", f"{self.url}search/config/{model_id}", self.headers)
        result = res.json()
        del self.headers['Content-Type']
        self.id = model_id
        self.set_returned_data(result)
        return self

    def update(self, model_id: str, update_files: List) -> Model:
        """ Update model where model_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(model_id, str):
            raise QtArgumentError("Argument type error: String is expected as model_id")
        if not isinstance(update_files, List):
            raise QtArgumentError("Argument type error: List is expected as update file")
        else:
            self.clear()
            data = {tag_files: update_files}
        res = connect("post", f"{self.url}search/update/{model_id}", self.headers, "data", json.dumps(data))
        result = res.json()
        del self.headers['Content-Type']
        self.id = model_id
        self.set_returned_data(result)
        return self

    def clone(self, model_id: str) -> Model:
        """ Update model where model_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(model_id, str):
            raise QtArgumentError("Argument type error: String is expected as model_id")
        if tag_files not in self.temp_dictionary:
            raise QtModelError("Model: You have to add files using with_document method and Document class")
        data = {tag_files: self.temp_dictionary[tag_files]}
        res = connect("post", f"{self.url}search/new/{model_id}", self.headers, "data", json.dumps(data))
        result = res.json()
        self.id = model_id
        self.set_returned_data(result)
        del self.headers['Content-Type']
        return self

    def delete(self, model_id: str) -> bool:
        """Delete data container"""

        if not isinstance(model_id, str):
            raise QtArgumentError("Argument type error: String is expected as model_id")
        res = connect("delete", f"{self.url}search/{model_id}", self.headers)
        return res.ok

    def progress(self, model_id: str = None) -> Dict:
        """Show progress for submitted process"""

        url_path = "progress"
        if model_id is not None:
            if isinstance(model_id, str):
                url_path = f"{url_path}/{model_id}"
            else:
                raise QtArgumentError("Expected string")
        res = connect("get", f"{self.url}search/{url_path}", self.headers)
        return res.json()

    def wait_for_completion(self) -> None:
        """Wait for completion processes"""

        percentage = 0
        while percentage < 100:
            result = self.progress(self.id)
            percentage = result["progress"]
            print(f"Search progress {percentage}%")
            if percentage < 100:
                sleep(1)
        sleep(3)

    def search(self, model_id: str, param_from: int = 0, size: int = None, f1: int = None, f2: int = None) -> Dict:
        """Search full-text and faceted search"""

        if not isinstance(model_id, str):
            raise QtArgumentError("Argument type error: String is expected as model_id")
        if isinstance(param_from, int):
            parameters = [('from', param_from)]
        else:
            raise QtArgumentError("Argument type error: Integer is expected as parameter")
        if size is not None:
            if isinstance(size, int) and 0 < size <= 200:
                parameters.append(('size', size))
            else:
                raise QtArgumentError("Argument type error: Integer between 0 and 200 is expected as parameter")
        if f1 is not None and f2 is not None:
            parameters.append(('f', f1))
            parameters.append(('f', f2))
        elif f1 is None and f2 is None:
            pass
        else:
            raise QtArgumentError("Argument error: Query filters must be used in pairs")
        res = connect("get", f"{self.url}search/{model_id}", self.headers, "params", parameters)

        return res.json()

    def read(self) -> List:
        """ Fetch model where model_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        res = connect("get", f"{self.url}users/profile", self.headers)
        re_dict = res.json()
        del self.headers['Content-Type']
        if "settings" in re_dict:
            model_list = []
            for i in re_dict["settings"]:
                model = Model()
                if "files" in i:
                    document_list = []
                    for f in i["files"]:
                        document = Document()
                        document.set_id(f)
                        document_list.append(document)
                    model.with_documents(document_list)
                model.set_id(i["id"])
                model.set_description(i["title"])
                model.set_workers(i["numWorkers"])
                if "searchDictionaries" in i:
                    for ex in i["searchDictionaries"]:
                        model.get_extractor(ex)
                model_list.append(model)
        else:
            model_list = []
        return model_list
