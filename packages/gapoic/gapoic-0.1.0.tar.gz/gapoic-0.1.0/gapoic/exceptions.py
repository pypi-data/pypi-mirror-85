""" ABS exceptions
"""


class ReadonlyException(Exception):
    """Raise when user is trying to set value on a readonly property"""

    def __init__(self, some_class_property):
        self.message = f"{some_class_property} is READ-ONLY"
        super().__init__(self.message)


class InvalidDataTypeException(Exception):
    """Raise when user is passing a value of non-acceptable data type"""

    def __init__(self, some_type):
        self.message = f"Only value of {some_type} is ACCEPTED"
        super().__init__(self.message)
