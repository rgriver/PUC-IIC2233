class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self, *elements):
        self.head = None
        self.tail = None
        for e in elements:
            self.add_tail(e)

    def initialize_list(self):
        self.head = None
        self.tail = None

    def add_tail(self, data):
        node = Node(data)
        node.next = None
        if not self.head:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def remove_element(self, node):
        if node is self.head.data:
            if self.head.next is None:
                self.head = self.tail = None
            else:
                self.head = self.head.next
        else:
            current = self.head
            while current is not None and current.next.data is not node:
                current = current.next
            if current is not None:
                current.next = current.next.next


    def __repr__(self):
        msg = ''
        current = self.head
        while current is not None:
            msg += str(current.data) + '\n'
            current = current.next
        return msg

    def __getitem__(self, item):
        current = self.head
        for i in range(item):
            if current:
                current = current.next
            else:
                raise IndexError
        if not current:
            raise IndexError
        else:
            return current.data

    def __setitem__(self, key, value):
        current = self.head
        for i in range(key):
            if current:
                current = current.next
            else:
                raise IndexError
        current.data = value

    def __len__(self):
        length = 0
        current = self.head
        while current is not None:
            current = current.next
            length += 1
        return length

    def add_list(self, list_to_add):
        for element in list_to_add:
            if element not in self:
                self.add_tail(element)

    def sort(self):
        for i in range(1, len(self)):
            value = self[i]
            j = i - 1
            while j >= 0 and self[j] > value:
                self[j + 1] = self[j]
                j -= 1
            self[j + 1] = value
