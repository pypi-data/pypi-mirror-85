""" Least-Recently-Used In-Process Caching
"""
from typing import Tuple, Optional
from gapoic.abs import DoublyLinkedList, Node
from gapoic.exceptions import ReadonlyException


class LRU:
    """LRU that accepts flexible data"""

    def __init__(self, name: str = "", *, limit: int = 0):
        if not isinstance(limit, int):
            raise ValueError("Invalid lru max-size")

        if limit < 1:
            raise ValueError("Invalid lru max-size")

        self.__limit = limit
        self.__ll = DoublyLinkedList()
        self.__map = dict()
        self.__name = name
        self.__tail = None

    def __str__(self):
        ll_as_str = str(self.__ll)
        return ll_as_str

    def __getitem__(self, key) -> Optional[Node]:
        """short-syntax for access node in lru"""
        return self.get(key)

    def get(self, key) -> Optional[Node]:
        """Get a node from lru"""
        node = self.__map.get(key)

        if not node:
            return None

        # NOTE: move node to top:
        if self.__ll.head is not node:
            node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev
            else:
                self.__tail = node.prev
            node.next = self.__ll.head
            self.__ll.head.prev = node
            self.__ll.head = node
            node.prev = None

        return node

    def put(self, key, data) -> Optional[Node]:
        """Putting data in LRU
        - if existing data, move it to top of the list
        - if non-exist, create new node if limit is
        not reached and insert it at the head of the list
        - return the evicted node if neccessary
        """
        node = self.__map.get(key)

        if not node:
            node = Node(key, data, mutable=True)
            self.__map.update({key: node})

            if self.__ll.head:
                node.next = self.__ll.head
                self.__ll.head.prev = node

            self.__ll.head = node
        else:
            node.data = data

            if self.__ll.head is not node:
                node.prev.next = node.next
                if node.next:
                    node.next.prev = node.prev
                else:
                    self.__tail = node.prev
                node.next = self.__ll.head
                self.__ll.head.prev = node
                self.__ll.head = node
                node.prev = None

        if not self.__tail:
            self.__tail = self.__ll.head

        if self.size > self.limit:
            tail = self.__tail
            self.__tail = tail.prev
            self.__tail.next = None

            del self.__map[tail.key]
            return tail
        return None

    @property
    def limit(self):
        """Maximum number of node that the LRU can hold"""
        return self.__limit

    @limit.setter
    def limit(self, _):
        """read-only"""
        raise ReadonlyException("LRU's limit")

    @property
    def size(self):
        """Current number of nodes that the LRU is keeping"""
        return len(self.__map)

    @size.setter
    def size(self, _):
        """read-only"""
        raise ReadonlyException("LRU's size")

    def link_ends(self) -> Tuple[Optional[Node], Optional[Node]]:
        """Used for debugging mostly
        return an immutable copy of head & tail of the lru
        """
        if not self.__ll.head:
            return None, None

        copied_head = Node(self.__ll.head.key, self.__ll.head.data)
        copied_tail = Node(self.__tail.key, self.__tail.data)
        return copied_head, copied_tail
