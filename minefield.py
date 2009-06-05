
import sys
import random

class MineField(object):

    MINE = '*'

    def __init__(self, width, height, minecount=None):
        self.width = width
        self.height = height
        self.minecount = minecount
        self.field = [' '] * height * width
        self._put_mines()
        self._compute_counters()

    def _is_mine(self, i):
        return self.field[i] == self.MINE

    def _put_mines(self):
        random.seed()
        l = random.sample(range(self.height * self.width), self.minecount)
        for i in l:
            self.field[i] = self.MINE

    def _compute_counters(self):
        w = self.width
        h = self.height

        i = 0
        while i < len(self.field):
            if self._is_mine(i):
                i += 1
                continue
            
            result = 0
            x = i % w
            y = i / w

            if x > 0:
                if self._is_mine(i - 1):
                    result += 1
            if y > 0:
                if self._is_mine(i - w):
                    result += 1
            if x < w - 1:
                if self._is_mine(i + 1):
                    result += 1
            if y < h - 1:
                if self._is_mine(i + w):
                    result += 1

            if x > 0 and y > 0:
                if self._is_mine(i - 1 - w):
                    result += 1
            if x < w - 1 and y > 0:
                if self._is_mine(i + 1 - w):
                    result += 1
            if x < w - 1 and y < h - 1:
                if self._is_mine(i + 1 + w):
                    result += 1
            if x > 0 and y < h - 1:
                if self._is_mine(i - 1 + w):
                    result += 1

            self.field[i] = str(result)
            i += 1

    def size(self):
        return self.width, self.height

    def get_mine_count(self):
        return self.minecount

    def get_cell(self, x, y):
        return self.field[x + y * self.width]

    def dump(self):
        l = self.field
        while len(l) > 0:
            print ' '.join(l[:self.width])
            del l[:self.width]


def main(argv=None):
    ms = MineField(5, 5, 1)
    ms.dump()
    print
    ms = MineField(5, 5, 5)
    ms.dump()
    print
    ms = MineField(5, 5, 15)
    ms.dump()
    print
    ms = MineField(20, 15, 40)
    ms.dump()


if __name__ == "__main__":
    main(sys.argv)

