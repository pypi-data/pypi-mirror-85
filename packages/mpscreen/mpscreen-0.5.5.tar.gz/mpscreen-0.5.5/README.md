## Info

mpscreen is a tool for screen manipulation. It allows for multiple consoles, dividing screen, custom colors and supports 
multiprocess environments. It uses ASCI escape codes so will work on linux only. If your console is set up for 256 colors
 
## Usage

In order to use this first setup screen server and build elements. Once build you must start the server.

```python
# build screen server
ss = mpscreen() 

# build screen elements
l1 = ss.buildLine(top=1, pattern=[" Main Pattern : ", Vstr("v:<13")], background=52, color=207) # adding custom elements
l2 = ss.buildLine(top=2, pattern=[" Main Pattern  ", Vint("count:5"), ' / ', Vint("total:5")], background=55, color=207)
upperConsole = ss.buildBuffer(top=3, height=20)
lowerConsole = ss.buildBuffer(bottom=2, top=25, background = 117)

# start the server
ss.start() 
```

Now you can manipulate screen from any process. 

```python
def linePrinter(cs: line):
    for i in range(100, 200):
        cs.v = "xxx" + str(i) * 3
        time.sleep(0.2)


def linePrinter2(cs: line):
    cs.total = 200
    for i in range(0, 200):
        cs.count = i
        time.sleep(0.2)


def bufferPrinter(bs: buffer):
    for i in range(1000, 3000):
        bs.append(('\u001b[48;5;13m') + (str(i) * (2)))
        bs.append((str(i) * 13))
        time.sleep(0.1)

pr = [Process(target=linePrinter, args=[l1]),
      Process(target=linePrinter2, args=[l2]),
      Process(target=bufferPrinter, args=[upperConsole]),
      Process(target=bufferPrinter, args=[lowerConsole])]

for p in pr:
    p.start()

for p in pr:
    p.join()

ss.close()
```