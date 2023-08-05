""" Typical Linkedlist Node
"""
from gapoic.exceptions import (
    ReadonlyException,
    InvalidDataTypeException,
)


class Node:
    """Node instance can hold any kind of data
    - For doubly-linkedlist
    - By default, node's data is immutable
    """

    def __init__(self, key, data, mutable=False):
        self.__key = key
        self.__data = data
        self.__mutable = mutable
        self.__next: Node = None
        self.__prev: Node = None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        if not self.__mutable:
            raise ReadonlyException("Node's data")
        self.__data = data

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, _):
        raise ReadonlyException("Node's key")

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, some_node):
        if some_node is not None and not isinstance(some_node, self.__class__):
            raise InvalidDataTypeException(self.__class__)
        self.__next = some_node

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, some_node):
        if some_node is not None and not isinstance(some_node, self.__class__):
            raise InvalidDataTypeException(self.__class__)
        self.__prev = some_node
