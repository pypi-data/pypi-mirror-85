'''
Created on Aug 14, 2015
@author: hari
'''
from builtins import object
class Queue(object):
    """
    Implementation of queue in Python using list.
    """
    def __init__(self):
        self._list = []
    
    def enqueue(self, item):
        self._list.append(item)
    
    def dequeue(self):
        if len(self._list) == 0:
            return None
            
        item = self._list[0]
        del self._list[0]
        return item
    
    def __len__(self):
        return len(self._list)
    
    @property
    def size(self):
        return len(self._list)
    
    def __iter__(self):
        while len(self._list) != 0:
            yield self.dequeue()

    @property
    def front(self):
        if len(self._list) == 0:
            return None
        return self._list[0]
    
    def __str__(self):
        return '%s size %s Q %s' % (self.__class__.__name__, len(self), self._list) 