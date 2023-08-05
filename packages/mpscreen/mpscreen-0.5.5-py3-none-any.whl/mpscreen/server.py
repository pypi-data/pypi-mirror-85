import os
import time
from multiprocessing import Queue
from multiprocessing import Process
from queue import Empty

from mpscreen.components import buffer, bufferServer, line, lineServer, Vstr, Vint, SR, SL

consoleEscape = r'\u001b\[.+m'

def _screenMainLoop(s):
    s.getTerminalSize()
    s.refresh(f=True)
    resizeCheck = int(round(time.time() * 1000))
    while True:
        if int(round(time.time() * 1000)) - resizeCheck > 1000:
            s.getTerminalSize()
            resizeCheck = int(round(time.time() * 1000))
            s.refresh(f=True)
        try:
            msg = s.q.get(timeout=0.5)
        except Empty:
            s.refresh()

        if msg[0] == 'Q':
            return
        elem = s._getElem(msg[0])
        if elem:
            elem.receive(msg[1:])
            s.refresh()



class server:
    def __init__(self):
        self.q = Queue()
        self.state = {}
        self._p = None
        self.elems = {}
        self.rows = 20
        self.columns = 80
        self.getTerminalSize()


    def start(self):
        self._p = Process(target=_screenMainLoop, args=(self,))
        self._p.start()

    def buildBuffer(self, top=None, bottom=None, height=None, color=249, background=235):
        id = len(self.elems)
        element = bufferServer(top=top, bottom=bottom, height=height, color=color, background=background)
        self.elems[id] = element
        return buffer(self.q, id)

    def buildLine(self,top=None, bottom=None, pattern=[''], background=40, color=50):
        id = len(self.elems)
        element = lineServer(top=top, bottom=bottom, pattern=pattern, background=background, color=color)
        self.elems[id] = element
        return line(self.q, id, element.variables)

    def _getElem(self, elem):
        if elem in self.elems:
            return self.elems[elem]
        return None

    def refresh(self, f=False):
        if f:
            print("\u001b[2J")
        for v in self.elems.values():
            v.paint(rows=self.rows, columns=self.columns, f=f)
        print('\u001b[{};0H'.format(self.rows - 1))

    def getTerminalSize(self):
        rc = []
        try:
            rc = os.popen('stty size', 'r').read().split()
        except:
            pass
        if len(rc) > 0:
            if self.rows != int(rc[0]) or self.columns != int(rc[1]):
                self.refresh(f=True)
            self.rows = int(rc[0])
            self.columns = int(rc[1])

    def close(self):
        self.q.put(['Q'])


def linePrinter(cs: line):
    for i in range(50, 300):
        cs["v"].set("xxx" + str(i) * 3)
        time.sleep(2.2)


def linePrinter2(cs: line):
    cs.total = 200
    for i in range(0, 2000):
        cs["count"].add(1)
        time.sleep(1.2)


def bufferPrinter(bs: buffer):
    for i in range(1000, 3000):
        bs.append(('\u001b[48;5;13m') + (str(i) * (2)))
        bs.append((str(i) * 13))
        time.sleep(1.1)



if __name__ == "__main__":
    ss = server()
    l1 = ss.buildLine(top=1, pattern=[" Main Pattern : ", SR(background=240), "  ",Vstr("v"),"  "], background=52, color=207)
    l2 = ss.buildLine(top=2, pattern=[" Main Pattern  ", SR(background=240), Vint("count:>8")," ", SR(background=245), Vint("total:>8")," "], background=55, color=207)
    upperConsole = ss.buildBuffer(top=3, height=20)
    lowerConsole = ss.buildBuffer(bottom=2, top=25, background = 117)
    ss.buildLine(top=24, background=24)
    ss.buildLine(bottom=1, background=24)
    ss.start()



    pr = [Process(target=linePrinter, args=[l1]),
          Process(target=linePrinter2, args=[l2]),
          Process(target=bufferPrinter, args=[upperConsole]),
          Process(target=bufferPrinter, args=[lowerConsole])
    ]

    for p in pr:
        p.start()

    for p in pr:
        p.join()

    ss.close()
