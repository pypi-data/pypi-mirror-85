from __future__ import annotations
from qtcurate.document import Document
from qtcurate.extractor import Extractor, Mode, ChunkMode, SearchMode, AnalyzeMode
from qtcurate.connect import connect, json_to_tuple
from time import sleep
import re
import json
from typing import Dict, List
from qtcurate.qt import Qt
from qtcurate.exceptions import QtArgumentError, QtModelError


tag_files = "files"
chunk = "chunk"
num_workers = "numWorkers"
tag_title = "title"
vocab_id = "vocabId"
vocab_value_type = "vocabValueType"
validator = "phraseMatchingPattern"
phrase_groups = "phraseMatchingGroups"
tag_exclude_utt = "excludeUttWithoutEntities"
tag_search_dict = "searchDictionaries"
between_values = "skipPatternBetweenValuess"
search_mod = "searchMode"
analyze_strategy = "analyzeStrategy"
stop_word_list = "stopwordList"
synonym_l = "synonymList"
type = "dataType"
language = "language"


class DataProcess:
    def __init__(self):
        self.headers = {"X-API-Key": Qt.api_key}
        self.temp_dict = dict()
        self.temp_dict[tag_exclude_utt] = True
        self.temp_dict[num_workers] = 8
        self.temp_dict[chunk] = ChunkMode.PAGE.value
        self.temp_dict[tag_search_dict] = []
        self.index = None
        self.uuid = None
        self.id = None
        self.url = Qt.url

    def __repr__(self):
        return f"{self.id}"

    def get_id(self):
        return str(self.id)

    def set_id(self, vocabulary_id: str) -> None:
        self.id = vocabulary_id

    def set_chunk(self, value: ChunkMode) -> None:
        self.temp_dict[chunk] = value.value

    def set_language(self, lang: str) -> DataProcess:
        self.temp_dict[language] = lang
        return self


    def get_uuid(self):
        return str(self.uuid)

    def set_description(self, title: str) -> None:
        """Create title for mining data"""

        if isinstance(title, str):
            self.temp_dict[tag_title] = title
        else:
            raise QtArgumentError("Argument type error: String is expected as description")

    def exclude_utt_without_entities(self, value: bool) -> None:
        """Set exclude utt for mining data, this is optional parameter"""

        if isinstance(value, bool):
            self.temp_dict[tag_exclude_utt] = value
        else:
            raise QtArgumentError("Argument type error: Boolean is expected as exclude utt without entities")

    def set_workers(self, value: int) -> None:
        if isinstance(value, int):
            self.temp_dict[num_workers] = value
        else:
            raise QtArgumentError("Argument type error: Integer is expected as num_workers")

    def with_documents(self, list_of_files: list) -> None:
        """Create a list of existing files"""

        if isinstance(list_of_files, list):
            self.temp_dict[tag_files] = list_of_files
        else:
            raise QtArgumentError("Argument type error: Expected list of file IDs")

    def add_extractor(self, extractor: Extractor) -> DataProcess:
        """Prepare dictionary for searching"""
        vocab_dict = dict()
        if extractor.get_vocab_id() is not None:
            vocab_dict[vocab_id] = extractor.get_vocab_id()
        if extractor.get_vocab_value_type() is not None:
            vocab_dict[vocab_value_type] = extractor.get_vocab_value_type()
        if extractor.get_type() is not None:
            vocab_dict[type] = extractor.get_type().value
        if extractor.get_mode() is None and extractor.get_analyze_mode() is None and extractor.get_search_mode() is None:
            vocab_dict[search_mod] = SearchMode.ORDERED_SPAN.value
            vocab_dict[analyze_strategy] = AnalyzeMode.SIMPLE.value
        elif extractor.get_mode() is not None and extractor.get_analyze_mode() is None and extractor.get_search_mode() is None:
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
        elif extractor.get_mode() is None and extractor.get_search_mode() is not None and extractor.get_analyze_mode() is not None:
            vocab_dict[search_mod] = extractor.get_search_mode().value
            vocab_dict[search_mod] = extractor.get_analyze_mode().value
        elif extractor.get_mode() is None and extractor.get_search_mode() is None and extractor.get_analyze_mode() is not None:
            vocab_dict[search_mod] = extractor.get_analyze_mode().value
        elif extractor.get_mode() is None and extractor.get_search_mode() is not None and extractor.get_analyze_mode() is None:
            vocab_dict[search_mod] = extractor.get_search_mode().value
        else:
            raise QtModelError("QtDataProcess error: Please do not set DataMode and (AnalyzeMode and SearchMode) in same time")
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
        self.temp_dict[tag_search_dict].append(vocab_dict)
        return self

    def get_extractor(self, dictionary: Dict) -> DataProcess:
        if tag_search_dict in dictionary:
            for i in dictionary[tag_search_dict]:
                self.temp_dict[tag_search_dict].append(i)
        return self

    def clear(self) -> None:
        """Remove all temporary data"""
        self.temp_dict.pop(tag_files, None)
        self.temp_dict.pop(tag_title, None)
        self.temp_dict[tag_exclude_utt] = True
        self.temp_dict[num_workers] = 4
        self.temp_dict.pop(tag_search_dict, None)
        self.index = None

    def create(self) -> Dict:
        """Mine data via dictionaries"""

        self.headers["Content-Type"] = "application/json"
        correct = 0
        if len(self.temp_dict[tag_search_dict]) == 0:
            raise QtModelError("DataProcess error: Please add parameters using add_extractor function")
        if tag_files in self.temp_dict and len(self.temp_dict[tag_files]) > 0:
            data = {tag_files: self.temp_dict[tag_files]}
        data[tag_exclude_utt] = self.temp_dict[tag_exclude_utt]
        data[num_workers] = self.temp_dict[num_workers]
        data[chunk] = self.temp_dict[chunk]
        if len(self.temp_dict[tag_search_dict]) != 0:
            data[tag_search_dict] = self.temp_dict[tag_search_dict]
        if tag_title in self.temp_dict:
            data[tag_title] = self.temp_dict[tag_title]
        res = connect("post", f"{self.url}search/new", self.headers, "data", json.dumps(data))
        self.id = res.json()['id']
        del self.headers['Content-Type']
        return json_to_tuple(res.json())

    def fetch(self, dp_id: str) -> Dict:
        """ Fetch dataprocess where dp_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        res = connect("get", f"{self.url}search/config/{dp_id}", self.headers)
        del self.headers['Content-Type']
        return res.json()

    def update(self, dp_id: str, update_files: List) -> Dict:
        """ Update dataprocess where dp_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        if not isinstance(update_files, List):
            raise QtArgumentError("Argument type error: List is expected as update file")
        else:
            self.clear()
            data = {tag_files: update_files}
        res = connect("post", f"{self.url}search/update/{dp_id}", self.headers, "data", json.dumps(data))
        del self.headers['Content-Type']
        return json_to_tuple(res.json())

    def clone(self, dp_id: str) -> Dict:
        """ Update dataprocess where dp_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        else:
            data = {tag_files: self.temp_dict[tag_files]}
        res = connect("post", f"{self.url}search/new/{dp_id}", self.headers, "data", json.dumps(data))
        self.id = res.json()['id']
        del self.headers['Content-Type']
        return json_to_tuple(res.json())

    def delete(self, dp_id: str) -> bool:
        """Delete data container"""

        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        res = connect("delete", f"{self.url}search/{dp_id}", self.headers)
        return res.ok

    def progress(self, dp_id: str = None) -> Dict:
        """Show progress for submitted data mining job"""

        url_path = "progress"
        if dp_id is not None:
            if isinstance(dp_id, str):
                url_path = f"{url_path}/{dp_id}"
            else:
                raise QtArgumentError("Expected string")
        res = connect("get", f"{self.url}search/{url_path}", self.headers)
        return json_to_tuple(res.json())

    def wait_for_completion(self):
        percentage = 0
        while percentage < 100:
            result = self.progress(self.id)
            percentage = result.progress
            print(f"Search progress {percentage}%")
            if percentage < 100:
                sleep(1)
        sleep(3)

    def search(self, dp_id: str, param_from: int = 0, size: int = None, f1: int = None, f2: int = None) -> Dict:
        """Search full-text and faceted search"""

        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
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
        res = connect("get", f"{self.url}search/{dp_id}", self.headers, "params", parameters)

        return json_to_tuple(res.json())

    def read(self):
        """ Fetch dataprocess where dp_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        res = connect("get", f"{self.url}users/profile", self.headers)
        re_dict = res.json()
        del self.headers['Content-Type']
        if "settings" in re_dict:

            dataprocess_list = []
            for i in re_dict["settings"]:
                dataprocess = DataProcess()
                if "files" in i:
                    document_list = []
                    for f in i["files"]:
                        document = Document()
                        document.set_id(f)
                        document_list.append(document)
                dataprocess.with_documents(document_list)
                dataprocess.set_id(i["id"])
                dataprocess.set_description(i["title"])
                dataprocess.set_workers(i["numWorkers"])
                extractor_list = []
                if "searchDictionaries" in i:
                    for ex in i["searchDictionaries"]:
                        dataprocess.get_extractor(ex)
                dataprocess_list.append(dataprocess)

        return dataprocess_list
