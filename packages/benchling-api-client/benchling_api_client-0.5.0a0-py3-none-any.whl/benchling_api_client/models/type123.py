from enum import Enum


class Type123(str, Enum):
    TEXT = "text"
    CODE = "code"
    TABLE = "table"
    LIST_BULLET = "list_bullet"
    LIST_NUMBER = "list_number"
    LIST_CHECKBOX = "list_checkbox"
    EXTERNAL_FILE = "external_file"
