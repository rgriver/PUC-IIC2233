from linked_list import *

class CountryList(LinkedList):
    def __init__(self, *elements):
        super(WorldConnections, self).__init__(elements)

    def __getitem__(self, item):
        current = self.head
        while current.data.name != item:
            current = current.next
        return current.data
