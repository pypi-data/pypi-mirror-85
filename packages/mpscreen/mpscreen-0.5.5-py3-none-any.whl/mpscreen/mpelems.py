import sys
import re
from enum import Enum
from multiprocessing import Queue


class Align(Enum):
    Left = 0
    Right = 1
    Center = 2


def stringLen(s):
    return len(re.sub("\u001b\[[0-9;]+.", '', s))


def fillSpaces(s, w, a= Align.Left):
    while stringLen(s) > w:
        s = s[1:]
    if a is None or a == Align.Left:
        s = s + ' ' * (w - stringLen(s))
    elif a == Align.Right:
        s = s + ' ' * (w - stringLen(s))
    else:
        sl = (w - stringLen(s)) // 2
        sr = w - stringLen(s) - sl
        s = (' ' * sl ) + s + (' ' * sr)

    return s


def colorCode(bg, fg):
    return '\u001b[48;5;{bg}m\u001b[38;5;{fg}m'.format(bg=bg, fg=fg)


def leftArrow(bgCode, fgCode):
    return '\u001b[38;5;{bg}m\uE0B2\u001b[48;5;{bg}m\u001b[38;5;{fg}m'.format(bg=bgCode, fg=fgCode)


def sanitize(pattern):
    pattern = pattern.replace("{{", "")
    pattern = pattern.replace("}}", "")
    return pattern


def fill(pattern, data):
    while True:
        try:
            result = pattern.format(*data)
            return result
        except:
            data.append('')


def placeholders(pattern):
    # print(pattern)
    pattern = sanitize(pattern)
    # print(pattern)

    phRegex = "{[^{}]*}"
    inner = re.findall(phRegex, pattern)
    # print(inner)
    for ip in inner:
        patern = pattern.replace(ip[1], '')
    # print(patern)
    outer = re.findall(phRegex, patern)
    # print(outer)
    return len(inner) + len(outer)


# TEXT VARIABLES

class _S:
    def __init__(self, align: Align, color, background):
        self.align = align
        self.color = color
        self.background = background


class SL(_S):
    def __init__(self, color=15, background=50):
        super().__init__(Align.Left, color=color, background=background)


class SR(_S):
    def __init__(self, color=15, background=50):
        super().__init__(Align.Right, color=color, background=background)


class _Val:
    def __init__(self, name):
        parts = name.split(":")
        self.name = parts[0]
        self.align = None

        if len(parts) > 0 and parts[1].strip()[0] in ["<","^",">"]:
            alignSign = parts[1].strip()[0]
            if alignSign == "<":
                self.align = Align.Left
            elif alignSign == ">":
                self.align = Align.Right
            elif alignSign == "^":
                self.align = Align.Center
        if len(parts) > 0:
            m = re.search(r'\d+$', parts[1].strip())
            if m is not None:
                self.width = int(m.group())


class Vstr(_Val):
    def __init__(self, name):
        super().__init__(name)


class Vint(_Val):
    def __init__(self, name):
        super().__init__(name)


# CLIENTS

class line:
    def __init__(self, q : Queue, id, attributes):
        self.q = q
        self.id = id
        self.attributes = attributes

    def __setattr__(self, key, value):
        if key in ["q", "id", "attributes"]:
            self.__dict__[key] = value
        else:
            if key in self.attributes:
                self.q.put([self.id, key, False, value])

    def __setitem__(self, item, val):
        self.__setattr__(item, val)

    def __getitem__(self, item):
        return type("rtVal",(),
                    {
                        "add": lambda v:  self.q.put([self.id, item, True, v]),
                        "set": lambda v : self.q.put([self.id, item, False, v])
                    })





class buffer:
    def __init__(self, q : Queue, id):
        self.q = q
        self.id = id

    def append(self, message):
        self.q.put([self.id, True, message])

    def clear(self, message):
        self.q.put([self.id, False, message])


# SERVERS


class Elem:
    def __init__(self):
        self.needsPainting = True

    def paint(self, rows, columns, f=False):
        if self.needsPainting or f:
            self._paint(rows=rows, columns=columns)
            self.needsPainting = False

    def receive(self, data):
        self.needsPainting = True
        self._receive(data)


class bufferServer(Elem):
    def __init__(self, top=None, bottom=None, height=None, color=249, background=235):
        super().__init__()
        if top and bottom and height:
            raise Exception("All top, bottom and height setup")
        if not top and not bottom and not height:
            self.top = 0
            self.bottom = 1
        elif len(list(filter(lambda x: x is not None, [top, bottom, height]))) < 2:
            if not top:
                top = 0
            else:
                bottom = 1

        self.top = max(0, top) if top is not None else None
        self.bottom = max(1, bottom) if bottom is not None else None
        self.height = max(1, height) if height is not None else None

        self.lines = []
        self.color = color
        self.background = background

    def _receive(self, messageArray):
        if messageArray[0]:
            self.lines.append(messageArray[1])
            if len(self.lines) > 100:
                self.lines = self.lines[-100:]
        else:
            self.lines = []

    def _colorCode(self):
        return colorCode(self.background, self.color)

    def _paint(self, rows, columns):
        bottom = rows - self.bottom if self.bottom is not None else min(rows - 1, self.top + self.height)
        bottom += 1
        top = self.top if self.top is not None else max(0, rows - (self.bottom + self.height - 1))
        for b in reversed(self.lines):
            realLen = stringLen(b)
            lines = (realLen + columns - 1) // columns
            bottom -= lines
            if bottom < top:
                break
            insert = str(b) + self._colorCode() + " " * ((lines * columns) - realLen)
            line = '\u001b[{row};0H' + self._colorCode() + insert + '\u001b[0m'
            print(line
                  .format(row=bottom, message=b, width=columns, fg=self.color, bg=self.background), end="")
            sys.stdout.flush()


class lineServer(Elem):
    def __init__(self, top=None, bottom=None, pattern=[''], background=40, color=50):
        super().__init__()
        if top is None and bottom is None:
            top = 1
        self.top = top
        self.bottom = bottom
        self.pattern = pattern
        self.background = background
        self.color = color
        self.dataArray = []
        self.variables = {}
        for v in filter(lambda x: isinstance(x, _Val), self.pattern):
            if isinstance(v, Vstr):
                self.variables[v.name] = ""
            elif isinstance(v, Vint):
                self.variables[v.name] = 0

    def _receive(self, data):
        if data[1]:
            self.variables[data[0]] += data[2]
        else:
            self.variables[data[0]] = data[2]

    def _getDataChunk(self, i):
        if len(self.dataArray) > i:
            return self.dataArray[i]
        return []

    def _getColor(self, i):
        if len(self.colors) > i:
            return self.colors[i]
        return 12, 30

    def _renderVar(self, x: _Val):
        buf = []
        if isinstance(x, Vstr):
            buf.append(self.variables[x.name])
        elif isinstance(x, Vint):
            buf.append(str(self.variables[x.name]))
        if x.width is not None:
            buf.append(fillSpaces(''.join(buf), x.width, x.align))
        return ''.join(buf)

    def _renderPattern(self, p):
        buf = []
        for x in p:
            if isinstance(x, str):
                buf.append(x)
            elif isinstance(x, _Val):
                buf.append(self._renderVar(x))
        return ''.join(buf)

    def _enumInstances(self, t):
        res = []
        for i, v in enumerate(self.pattern):
            if isinstance(v, t):
                res.append(i)
        return res

    def _buildSuffix(self):
        suffix = []
        ssi = self._enumInstances(SR)
        end = len(self.pattern)
        #print("*****")
        #print("pattern", self.pattern, len(self.pattern))
        #print("SSI", ssi)
        for i in reversed(ssi):
            pieces = self.pattern[i+1: end]
            #print("Pieces", pieces)
            if len(pieces) > 0:
                suffix.append(self._renderPattern(pieces))
                split : SR = self.pattern[i]
                suffix.append(leftArrow(bgCode=split.background, fgCode=split.color))
            #print("suffix", suffix)
            end = i
        return ''.join(reversed(suffix)), ssi[0] if len(ssi) > 0 else len(self.pattern)

    def _paint(self, rows, columns):
        suffixStr, suffixStart = self._buildSuffix()
        #print("fullsuffix",suffixStr)
        message = self._renderPattern(self.pattern[:suffixStart])
        message = fillSpaces(message, columns - stringLen(suffixStr))
        print('\u001b[{line};0H{cc}{message}{suffix}\u001b[0m'
              .format(message,
                      line=self.top if self.top is not None else rows - max(1, self.bottom),
                      cc=colorCode(bg=self.background, fg=self.color),
                      message=message,
                      suffix=suffixStr), end="")
