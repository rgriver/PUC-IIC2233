from linked_list import *


class MeasuresList(LinkedList):
    def __init__(self, *args):
        super(MeasuresList, self).__init__(*args)

    def add_tail(self, data):
        node = Node(data)
        node.next = None
        if not self.head:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def get_top(self):
        choice = LinkedList()
        index = len(self) - 1
        while index >= 0 and len(choice) < 3:
            choice.add_tail(self[index])
            index -= 1
        return choice

    def sort(self):
        for i in range(1, len(self)):
            measure = self[i]
            j = i - 1
            while j >= 0 and self[j].priority > measure.priority:
                self[j + 1] = self[j]
                j -= 1
            self[j + 1] = measure


