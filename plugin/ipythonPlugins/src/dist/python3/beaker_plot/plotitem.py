# Copyright 2014 TWO SIGMA OPEN SOURCE, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum
from datetime import datetime
import math
from .utils import *


def getColor(color):
  if isinstance(color, list):
    values = []
    for c in color:
      values.append(getColor(c))

    return values
  elif isinstance(color, Color):
    return color.value
  else:
    return color


class ShapeType(Enum):
  SQUARE = 1
  CIRCLE = 2
  TRIANGLE = 3
  DIAMOND = 4
  DCROSS = 5
  DOWNTRIANGLE = 5
  CROSS = 6
  DEFAULT = 7
  LEVEL = 8
  VLEVEL = 9
  LINECROSS = 10


class StrokeType(Enum):
  NONE = 1
  SOLID = 2
  DASH = 3
  DOT = 4
  DASHDOT = 5
  LONGDASH = 5


class Color:
  def __init__(self, r, g, b, a=255):
    self.value = ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)
    if self.value < 0:
      self.value = 0xFFFFFFFF + self.value + 1

  def hex(self):
    return '#%02x' % self.value


Color.white = Color(255, 255, 255)
Color.WHITE = Color.white
Color.lightGray = Color(192, 192, 192)
Color.LIGHT_GRAY = Color.lightGray
Color.gray = Color(128, 128, 128)
Color.GRAY = Color.gray
Color.darkGray = Color(64, 64, 64)
Color.DARK_GRAY = Color.darkGray
Color.black = Color(0, 0, 0)
Color.BLACK = Color.black
Color.red = Color(255, 0, 0)
Color.RED = Color.red
Color.pink = Color(255, 175, 175)
Color.PINK = Color.pink
Color.orange = Color(255, 200, 0)
Color.ORANGE = Color.orange
Color.yellow = Color(255, 255, 0)
Color.YELLOW = Color.yellow
Color.green = Color(0, 255, 0)
Color.GREEN = Color.green
Color.magenta = Color(255, 0, 255)
Color.MAGENTA = Color.magenta
Color.cyan = Color(0, 255, 255)
Color.CYAN = Color.cyan
Color.blue = Color(0, 0, 255)
Color.BLUE = Color.blue


class Graphics:
  def __init__(self, data=None):
    if data is None:
      data = {}
    self.visible = getValue(data, 'visible', True)
    self.yAxis = getValue(data, 'yAxis')


class ConstantLine(Graphics):
  def __init__(self, data=None):
    if data is None:
      data = {}
    Graphics.__init__(self, data)
    self.x = getValue(data, 'x')
    self.y = getValue(data, 'y')
    self.baseColor = getColor(getValue(data, 'color'))
    self.width = getValue(data, 'width', 1.5)
    self.style = getValue(data, 'style')
    self.showLabel = getValue(data, 'showLabel')


class ConstantBand(Graphics):
  def __init__(self, data=None):
    if data is None:
      data = {}
    Graphics.__init__(self, data)
    self.x = getValue(data, 'x')
    self.y = getValue(data, 'y')
    self.color = getColor(getValue(data, 'color', Color(0, 127, 255, 127)))


class XYGraphics(Graphics):
  def __init__(self, data=None):
    if data is None:
      data = {}
    Graphics.__init__(self, data)
    defY = getValue(data, 'y')
    if defY is not None:
      defX = list(range(0, len(defY)))
    else:
      defX = []

    self.x = getValue(data, 'x', defX)
    if self.x is not None:
      for idx in range(len(self.x)):
        x = self.x[idx]
        if isinstance(x, datetime):
          self.x[idx] = x.microsecond

    self.y = defY
    self.display_name = getValue(data, 'display_name')
    self.lodFilter = getValue(data, 'lodFilter')
    self.lodFilter = getValue(data, 'lodFilter')


class Line(XYGraphics):
  def __init__(self, data=None):
    if data is None:
      data = {}
    XYGraphics.__init__(self, data)
    self.width = getValue(data, 'width', 1.5)
    self.style = getValue(data, 'style')
    self.interpolation = getValue(data, 'interpolation')
    self.color = getColor(getValue(data, 'color'))

class BasedXYGraphics(XYGraphics):
  def __init__(self, data=None):
    if data is None:
      data = {}
    XYGraphics.__init__(self, data)
    base = getValue(data, 'base')
    if isinstance(base, list):
      self.bases = base
    else:
      self.base = getValue(data, 'base', 0)

class Bars(BasedXYGraphics):
  def __init__(self, data=None):
    if data is None:
      data = {}
    BasedXYGraphics.__init__(self, data)

    width = getValue(data, 'width')
    if isinstance(width, list):
      self.widths = width
    else:
      self.width = width

    color = getColor(getValue(data, 'color'))
    if isinstance(color, list):
      self.colors = color
    else:
      self.color = color

    outlineColor = getColor(getValue(data, 'outlineColor'))
    if isinstance(outlineColor, list):
      self.outline_colors = outlineColor
    else:
      self.outline_color = outlineColor

class Points(XYGraphics):
  def __init__(self, data=None):
    if data is None:
      data = {}
    XYGraphics.__init__(self, data)

    shape = getColor(getValue(data, 'shape'))
    if isinstance(shape, list):
      self.shapes = shape
    else:
      self.shape = getValue(data, 'shape', ShapeType.DEFAULT)

    size = getColor(getValue(data, 'size'))
    if isinstance(size, list):
      self.sizes = size
    else:
      self.size = getValue(data, 'size', 0.6)

    fill = getColor(getValue(data, 'fill'))
    if isinstance(fill, list):
      self.fills = fill
    else:
      self.fill = fill

    color = getColor(getValue(data, 'color'))
    if isinstance(color, list):
      self.colors = color
    else:
      self.color = color

    outlineColor = getColor(getValue(data, 'outlineColor'))
    if isinstance(outlineColor, list):
      self.outline_colors = outlineColor
    else:
      self.outline_color = outlineColor

class Stems(BasedXYGraphics):
  def __init__(self, data=None):
    if data is None:
      data = {}
    BasedXYGraphics.__init__(self, data)
    self.width = getValue(data, 'width', 1.5)
    color = getColor(getValue(data, 'color'))
    if isinstance(color, list):
      self.colors = color
    else:
      self.color = color

    style = getValue(data, 'style')
    if isinstance(style, list):
      self.styles = style
    else:
      self.style = getValue(data, 'style', StrokeType.SOLID)

class Area(BasedXYGraphics):
  def __init__(self, data=None):
    if data is None:
      data = {}
    BasedXYGraphics.__init__(self, data)
    self.color = getColor(getValue(data, 'color'))
    self.interpolation = getValue(data, 'interpolation')

class Text():
  def __init__(self, data=None):
    if data is None:
      data = {}

    self.x = getValue(data, 'x', 0)
    self.y = getValue(data, 'y', 0)
    self.color = getColor(getValue(data, 'color'))
    self.size = getValue(data, 'size', 13)
    self.text = getValue(data, 'text', '')
    self.show_pointer = getValue(data, 'show_pointer', True)
    self.pointer_angle = getValue(data, 'pointer_angle', (-0.25) * math.pi)


class YAxis():
  def __init__(self, data=None):
    if data is None:
      data = {}
    self.label = getValue(data, 'label', '')
    self.autoRange = getValue(data, 'autoRange')
    self.color = getColor(getValue(data, 'color'))
    self.size = getValue(data, 'size', 13)
    self.text = getValue(data, 'text', '')
    self.show_pointer = getValue(data, 'show_pointer', True)
    self.pointer_angle = getValue(data, 'pointer_angle', (-0.25) * math.pi)

# TODO
# XYStacker
# Crosshair