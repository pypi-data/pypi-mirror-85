import os
import time
from multiprocessing import Queue
from multiprocessing import Process

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
        msg = s.q.get()

        if msg[0] == 'Q':
            return
        elem = s._getElem(msg[0])
        if elem:
            elem.receive(msg[1:])
            s.refresh()



class mpclient:
    def __init__(self, server):
        self.server = server

    def set(self, elem, line):
        self.server.q.put(['S', elem, line])

    def send(self, elem, line):
        self.server.q.put(['A', elem, line])


class mpscreen:
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

    def buildBuffer(self, **args):
        id = len(self.elems)
        element = bufferServer(**args)
        self.elems[id] = element
        return buffer(self.q, id)


    def buildLine(self, **args):
        id = len(self.elems)
        element = lineServer(**args)
        self.elems[id] = element
        return line(self.q, id, element.variables)

    def getElem(self, elem):
        if elem in self.elems:
            return self.elems[elem]
        return None

    def getClient(self):
        return mpclient(self)

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
        time.sleep(0.2)


def linePrinter2(cs: line):
    cs.total = 200
    for i in range(0, 2000):
        cs["count"].add(1)
        time.sleep(0.2)


def bufferPrinter(bs: buffer):
    for i in range(1000, 3000):
        bs.append(('\u001b[48;5;13m') + (str(i) * (2)))
        bs.append((str(i) * 13))
        time.sleep(0.1)



if __name__ == "__main__":
    ss = mpscreen()
    l1 = ss.buildLine(top=1, pattern=[" Main Pattern : ", SR(background=240), "  ",Vstr("v:^15"),"  "], background=52, color=207)
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
