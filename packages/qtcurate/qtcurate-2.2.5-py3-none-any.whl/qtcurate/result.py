from __future__ import annotations
import json
import os
from typing import List, Optional
from qtcurate.exceptions import QtArgumentError, QtFileTypeError
from qtcurate.qt import Qt
from qtcurate.connect import connect


NoneType = type(None)
category = "category"
vocab_name = "dict_name"
vocab_id = "dict_id"
type_field = "type"
str_field = "str"
double_value = "doubleValue"
int_value = "intValue"
line = "line"
start = "start"
end = "end"


class Position:
    def __init__(self):
        self.start = None
        self.end = None
        self.line = None

    def set_start(self, pos_start: Optional[int]) -> Position:
        """ Set start position"""

        if isinstance(pos_start, (int, NoneType)):
            self.start = pos_start
        else:
            raise QtArgumentError("Argument type error: Int is expected as pos_start")
        return self

    def get_start(self) -> Optional[int]:
        """Get start position"""

        return self.start

    def set_end(self, pos_end: Optional[int]) -> Position:
        """ Set end position"""

        if isinstance(pos_end, (int, NoneType)):
            self.end = pos_end
        else:
            raise QtArgumentError("Argument type error: Int is expected as pos_end")
        return self

    def get_end(self) -> Optional[int]:
        """Get end position"""

        return self.end

    def set_line(self, pos_line: Optional[int]) -> Position:
        """Set line position"""

        if isinstance(pos_line, (int, NoneType)):
            self.line = pos_line
        else:
            raise QtArgumentError("Argument type error: Int is expected as pos_line")
        return self

    def get_line(self) -> Optional[int]:
        """Get line position"""

        return self.line


class FieldValue:

    def __init__(self):
        self.str_value = None
        self.position = None

    def __repr__(self):
        return f"{self.str_value}"

    def set_str(self, str_val: Optional[str]) -> FieldValue:
        """Set str in FieldValue"""

        if isinstance(str_val, (str, NoneType)):
            self.str_value = str_val
        else:
            raise QtArgumentError("Argument type error: String is expected as str_val")
        return self

    def get_str(self) -> Optional[str]:
        """Get str in FieldValue"""

        return self.str_value

    def set_position(self, position: Optional[Position]) -> FieldValue:
        """Set position"""

        if isinstance(position, (Position, NoneType)):
            self.position = position
        else:
            raise QtArgumentError("Argument type error: Position is expected as position")
        return self

    def get_position(self) -> Optional[Position]:
        """Get position"""

        return self.position


class Field:
    def __init__(self):
        self.vocab_name = None
        self.vocab_id = None
        self.category = None
        self.type = None
        self.str = None
        self.values = None
        self.position = None

    def __repr__(self):
        return f"{self.vocab_id}, {self.str}"

    def set_values(self, val: Optional[List]) -> Field:
        """Set values in Field"""

        if isinstance(val, (list, NoneType)):
            self.values = val
        else:
            raise QtArgumentError("Argument type error: List is expected as val")
        return self

    def get_values(self) -> Optional[List]:
        """Set values in Field"""

        return self.values

    def set_str(self, str_value: Optional[str]) -> Field:
        """Set str in Field"""

        if isinstance(str_value, (str, NoneType)):
            self.str = str_value
        else:
            raise QtArgumentError("Argument type error: String is expected as str_val")
        return self

    def get_str(self) -> Optional[str]:
        """Get str in Field"""

        return self.str

    def set_type(self, type_value: Optional[str]) -> Field:
        """Set type in Field"""

        if isinstance(type_value, (str, NoneType)):
            self.type = type_value
        else:
            raise QtArgumentError("Argument type error: String is expected as type_value")
        return self

    def get_type(self) -> Optional[str]:
        """Get type in Field"""

        return self.type

    def set_vocab_name(self, name: Optional[str]) -> Field:
        """Set vocabulary name"""

        if isinstance(name, (str, NoneType)):
            self.vocab_name = name
        else:
            raise QtArgumentError("Argument type error: String is expected as name")
        return self

    def get_vocab_name(self) -> Optional[str]:
        """Get vocabulary name"""

        return self.vocab_name

    def set_category(self, cat: Optional[str]) -> Field:
        """Set category"""

        if isinstance(cat, (str, NoneType)):
            self.category = cat
        else:
            raise QtArgumentError("Argument type error: String is expected as cat")
        return self

    def get_category(self) -> Optional[str]:
        """Get category"""

        return self.category

    def set_vocab_id(self, voc_id: Optional[str]) -> Field:
        """Set vocabulary id"""

        if isinstance(voc_id, (str, NoneType)):
            self.vocab_id = voc_id
        else:
            raise QtArgumentError("Argument type error: String is expected as voc_id")
        return self

    def get_vocab_id(self) -> Optional[str]:
        """Get vocabulary id"""

        return self.vocab_id

    def set_position(self, position: Optional[Position]) -> Field:
        """Set position"""

        if isinstance(position, (Position, NoneType)):
            self.position = position
        else:
            raise QtArgumentError("Argument type error: Position is expected as position")
        return self

    def get_position(self) -> Optional[Position]:
        """Get position"""

        return self.position


class Result:
    def __init__(self, dp_id):
        self.id = dp_id
        self.headers = {"X-API-Key": Qt.api_key}
        self.url = Qt.url

    def raw_exporter(self, path: str) -> None:
        """Exporting in JSON format"""

        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".json":
            raise QtFileTypeError("File type error: Please use json extension saving file")
        res = connect("get", f"{self.url}reports/{self.id}/json", self.headers)
        with open(path, "w") as json_file:
            json.dump(res.json(), json_file)

    def result_xlsx_exporter(self, path: str) -> None:
        """Exporting in Excel format"""

        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".xlsx":
            raise QtFileTypeError("File type error: Please use xlsx extension saving file")
        res = connect("get", f"{self.url}reports/{self.id}/xlsx", self.headers)

        with open(path, 'wb') as excel_file:
            excel_file.write(res.content)

    def read(self) -> List:
        """Convert to easy readable list"""

        result_list = []
        res = connect("get", f"{self.url}reports/{self.id}/json", self.headers)
        for item in res.json():
            if "values" in item and item["values"]:
                for i in item["values"]:
                    field = Field()
                    position = Position()
                    if start in i:
                        position.set_start(i[start])
                    if end in i:
                        position.set_end(i[end])
                    if line in i:
                        position.set_line(i[line])
                    field.set_position(position)
                    if str_field in i:
                        field.set_str(i[str_field])
                    if type_field in i:
                        field.set_type(i[type_field])
                    if category in i:
                        field.set_category(i[category])
                    if vocab_name in i:
                        field.set_vocab_name(i[vocab_name])
                    if vocab_id in i:
                        field.set_vocab_id(i[vocab_id])
                    list_field_ext = []
                    if "extIntervalSimples" in i and i["extIntervalSimples"]:
                        for ext_int_item in i["extIntervalSimples"]:
                            field_value = FieldValue()
                            position_value = Position()
                            if start in ext_int_item:
                                position_value.set_start(ext_int_item[start])
                            if end in ext_int_item:
                                position_value.set_end(ext_int_item[end])
                            if line in ext_int_item:
                                position_value.set_line(ext_int_item[line])
                            field_value.set_position(position_value)
                            if str_field in ext_int_item:
                                field_value.set_str(ext_int_item[str_field])
                            list_field_ext.append(field_value)
                    field.set_values(list_field_ext)
                    result_list.append(field)
        return result_list
