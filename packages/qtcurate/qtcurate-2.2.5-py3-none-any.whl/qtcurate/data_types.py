from enum import Enum


class DictionaryType(Enum):
    NUMBER = "NUMBER"
    DATETIME = "DATETIME"
    REGEX = "REGEX"


class DataType(Enum):
    LONG = "LONG"
    KEYWORD = "KEYWORD"
    DATETIME = "DATETIME"
    STRING = "STRING"
    DOUBLE = "DOUBLE"
    PERCENT = "PERCENT"
    NOUN = "NOUN"


class HtmlParseMode(Enum):
    RAW = "RAW"
    SMART = "SMART"
    PLAIN = "PLAIN"
    HTML = "HTML"


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
