from tkinter import *
from math import sin, cos, pi
import random

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 8

def heart_function(t):
  x = 16 * pow(sin(t), 3)
  y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

  x *= IMAGE_ENLARGE
  y *= IMAGE_ENLARGE

  # shift
  x += CANVAS_CENTER_X
  y += CANVAS_CENTER_Y

  return int(x), int(y)

class Heart:
  def __init__(self):
      self.points = set()
      self.build(2000)

  def build(self, n):
     # Heart
     for i in range(n):
       t = random.uniform(0, 2 * pi)
       x, y = heart_function(t)
       self.points.add((x, y))

  def render(self, canvas):
      for x, y in self.points:
          canvas.create_rectangle(x, y, x+2, y+2, width=0, fill="#ff7171")

def draw(root: Tk, canvas: Canvas, heart: Heart):
    canvas.delete("all")
    heart.render(canvas)


if __name__ == "__main__":
  root = Tk()
  canvas = Canvas(root, bg="black", width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
  canvas.pack()
  heart = Heart()
  draw(root, canvas, heart)
  root.mainloop()
