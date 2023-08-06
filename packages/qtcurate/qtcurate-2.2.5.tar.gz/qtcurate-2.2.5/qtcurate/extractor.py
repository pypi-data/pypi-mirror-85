from __future__ import annotations
from enum import Enum
from qtcurate.exceptions import QtArgumentError
from typing import List


class ChunkMode(Enum):
    NONE = "NONE"
    SENTENCE = "SENTENCE"
    PAGE = "PAGE"


class SearchMode(Enum):
    ORDERED_SPAN = "ORDERED_SPAN"
    FUZZY_ORDERED_SPAN = "FUZZY_ORDERED_SPAN"
    SPAN = "SPAN"
    FUZZY_SPAN = "FUZZY_SPAN"
    PARTIAL_SPAN = "PARTIAL_SPAN"
    PARTIAL_FUZZY_SPAN = "PARTIAL_FUZZY_SPAN"


class AnalyzeMode(Enum):
    EXACT = "EXACT"
    EXACT_CI = "EXACT_CI"
    WHITESPACE = "WHITESPACE"
    SIMPLE = "SIMPLE"
    STANDARD = "STANDARD"
    LETTER = "LETTER"
    STEM = "STEM"


class Type(Enum):
    LONG = "LONG"
    DATETIME = "DATETIME"
    DOUBLE = "DOUBLE"


class Mode(Enum):
    SIMPLE = "SIMPLE"
    UNORDERED = "UNORDERED"
    STEM = "STEM"
    UNORDERED_STEM = "UNORDERED_STEM"
    FUZZY_UNORDERED_STEM = "FUZZY_UNORDERED_STEM"


class Extractor:
    def __init__(self):
        self.validator = None
        self.mode = Mode.SIMPLE
        self.type = None
        self.vocab_id = None
        self.vocab_value_type = None
        self.between_values = None
        self.stop_word_list = None
        self.synonym_list = None
        self.data_type = None

    def __repr__(self):
        return f"{self.validator} {self.mode}, {self.type}, {self.vocab_id}, {self.vocab_value_type} {self.data_type}"

    def create_mode(self, analyze_mode: AnalyzeMode, search_mode: SearchMode) -> Extractor:
        """Create mode"""

        if analyze_mode.value == "SIMPLE" and search_mode.value == "SPAN":
            self.mode = Mode.UNORDERED
        elif analyze_mode.value == "STEM" and search_mode.value == "ORDERED_SPAN":
            self.mode = Mode.STEM
        elif analyze_mode.value == "STEM" and search_mode.value == "SPAN":
            self.mode = Mode.UNORDERED_STEM
        elif analyze_mode.value == "STEM" and search_mode.value == "FUZZY_SPAN":
            self.mode = Mode.FUZZY_UNORDERED_STEM
        else:
            self.mode = Mode.SIMPLE
        return self

    def set_mode(self, mode: Mode) -> None:
        """Set mode"""

        if isinstance(mode, Mode):
            self.mode = mode
        else:
            raise QtArgumentError("Argument type error: Mode is expected as mode")

    def get_mode(self) -> Mode:
        """Get mode"""

        return self.mode

    def set_vocabulary(self, vocabulary: str) -> Extractor:
        """Set vocabulary id"""

        if isinstance(vocabulary, str):
            self.vocab_id = vocabulary
        else:
            raise QtArgumentError("Argument type error: String is expected as vocab_id")
        return self

    def get_vocab_id(self) -> str:
        """Get vocabulary id"""

        return self.vocab_id

    def get_vocab_value_type(self) -> str:
        """Get vocabulary value type"""

        return self.vocab_value_type

    def set_between_values(self, between_values: str) -> Extractor:
        """Set between values"""

        if isinstance(between_values, str):
            self.between_values = between_values
        else:
            raise QtArgumentError("Argument type error: String is expected as between_values")
        return self

    def get_between_values(self) -> str:
        """Get between values"""

        return self.between_values

    def set_type(self, data_type: Type) -> Extractor:
        """Set data type"""

        if isinstance(data_type, Type):
            self.type = data_type
        else:
            raise QtArgumentError("Argument type error: String is expected as DataType")
        return self

    def get_type(self) -> Type:
        """Get data type"""

        return self.type

    def set_stop_word_list(self, stop_word_list: List) -> Extractor:
        """ Set stop word list"""

        if isinstance(stop_word_list, list):
            self.stop_word_list = stop_word_list
        else:
            raise QtArgumentError("Argument type error: List is expected as stop_word_list")
        return self

    def get_stop_word_list(self) -> List:
        """Get stop word list"""

        return self.stop_word_list

    def set_synonym_list(self, synonym_list: List) -> Extractor:
        """Set synonym list"""

        if isinstance(synonym_list, list):
            self.synonym_list = synonym_list
        else:
            raise QtArgumentError("Argument type error: List is expected as synonym_list")

        return self

    def get_synonym_list(self) -> List:
        """Get synonym list"""

        return self.synonym_list

    def set_validator(self, validator: str) -> Extractor:
        """Set validator"""

        if isinstance(validator, str):
            self.validator = validator
            self.vocab_value_type = "REGEX"
        else:
            raise QtArgumentError("Argument type error: String is expected as validator")
        return self

    def get_validator(self) -> str:
        """Get validator"""

        return self.validator
