from pygame import Rect


class SquareRect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    @staticmethod
    def from_rect(rect, squaresize):
        return SquareRect(
            rect.left / squaresize,
            rect.top / squaresize,
            rect.width / squaresize,
            rect.height / squaresize,
        )

    def get_right(self):
        return self.left + self.width

    def set_right(self, value):
        self.left = value - self.width

    right = property(get_right, set_right)

    def get_bottom(self):
        return self.top + self.height

    def set_bottom(self, value):
        self.top = value - self.height

    bottom = property(get_bottom, set_bottom)

    def get_rect(self, squaresize):
        return Rect(
            int(self.left * squaresize),
            int(self.top * squaresize),
            int(self.width * squaresize),
            int(self.height * squaresize),
        )

    def copy(self):
        return SquareRect(self.left, self.top, self.width, self.height)
