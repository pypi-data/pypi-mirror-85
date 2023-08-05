"""Doubly-Linked-List"""
from typing import Optional
from gapoic.abs.node import Node
from gapoic.exceptions import InvalidDataTypeException


class DoublyLinkedList:
    """DoublyLinkedList"""

    def __init__(self, head: Node = None):
        self.__head = head

    def __str__(self):
        node: Optional[Node] = self.head
        text = ""

        while node:
            text += f"{node.key}"
            if node.next:
                text += " > "
            node = node.next

        return text

    @property
    def head(self):
        """return the head node of the linked-list"""
        return self.__head

    @head.setter
    def head(self, new_head: Optional[Node]):
        """change head, must be a Node"""
        if new_head is not None and not isinstance(new_head, Node):
            raise InvalidDataTypeException(Node)
        self.__head = new_head
