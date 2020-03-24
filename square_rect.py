from pygame import Rect

class SquareRect():
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def get_rect(self, squaresize):
        return Rect(
            int(self.left * squaresize),
            int(self.top * squaresize),
            int(self.width * squaresize),
            int(self.height * squaresize),
        )

    def copy(self):
        return SquareRect(self.left, self.top, self.width, self.height)