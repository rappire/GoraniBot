import random
from config import config


class Playlist:

    def __init__(self):
        self.play_que = []

    def add(self, track):
        self.play_que.append(track)

    def next(self):
        if len(self.play_que) == 0:
            return None
        return self.play_que.pop(0)

    def shuffle(self):
        random.shuffle(self.play_que)

    def move(self, oldindex: int, newindex: int):
        temp = self.play_que[oldindex]
        del self.play_que[oldindex]
        self.play_que.insert(newindex, temp)
        
    def delete(self, index : int):
        del self.play_que[index]

    def empty(self):
        self.play_que.clear()
    
    def isempty(self):
        if len(self.play_que) == 0:
            return True
        return False
    
    def length(self):
        return len(self.play_que)
