#!/usr/bin/env python

"""
Lyle Scott, III
lyle@digitalfoo.net

A simple demo that uses curses to scroll the terminal.
"""
import curses
import sys
import random
import time


class MenuDemo:
    DOWN = 1
    UP = -1
    SPACE_KEY = 32
    ESC_KEY = 27

    AUTOKEY = 65

    PREFIX_SELECTED = '_X_'
    PREFIX_DESELECTED = '___'

    outputLines = []
    screen = None
            
    def __init__(self):
        self.auto = False
        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        #self.screen.nodelay(1)
        (y,x) = self.screen.getmaxyx()
        self.COLS = x
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1) 
        self.screen.border(0)
        self.topLineNum = 0
        self.highlightLineNum = 0
        self.markedLineNums = []
        self.getOutputLines()
        self.updown(1)
        self.run()

    def run(self):
        while True:
            td = self.displayScreen()
            # get user command
            if self.auto:
                pass
                #self.updown(self.DOWN)
                #self.wait(td)

            c = self.screen.getch()
            if c == curses.KEY_UP: 
                self.updown(self.UP)
            elif c == curses.KEY_DOWN:
                self.updown(self.DOWN)
            elif c == self.SPACE_KEY:
                self.markLine()
            elif c == ord('a'):
                self.auto = not self.auto
                self.screen.addstr(0,0,"AUTO")
                self.screen.refresh()
                #time.sleep(2)
            elif c == self.ESC_KEY:
                self.exit()

    def wait(self, td):
        if td==1:
            time.sleep(5)
        else:
            time.sleep(td/15.0)

    def markLine(self):
        linenum = self.topLineNum + self.highlightLineNum
        if linenum in self.markedLineNums:
            self.markedLineNums.remove(linenum)
        else:
            self.markedLineNums.append(linenum)

    def getOutputLines(self):
        ### !!!
        ### This is where you would write a function to parse lines into rows 
        ### and columns. For this demo, I'll just create a bunch of random ints
        ### !!!
        self.outputLines = [x.strip() for x in open('mylines.txt').readlines()]
        self.nOutputLines = len(self.outputLines)

    def displayScreen(self):
        # clear screen
        self.screen.erase()
        td=0
        # now paint the rows
        top = self.topLineNum
        if top<=0:
            offset = -top
            bottom = curses.LINES-offset
            top = 0
        else:
            offset = 0
            bottom = self.topLineNum+curses.LINES

        for (index,line,) in enumerate(self.outputLines[top:bottom]):
            linenum = self.topLineNum + index
            if linenum in self.markedLineNums:
                prefix = self.PREFIX_SELECTED
            else:
                prefix = self.PREFIX_DESELECTED

            line = '%s %s' % (prefix, line,)

            # highlight current line            
            #if index != self.highlightLineNum:
            #self.screen.addstr(index+offset, 0, line, curses.color_pair(1))
            self.screen.addstr(index+offset, 0, line[0:self.COLS-1], curses.color_pair(1))
 
            if (index+offset) == curses.LINES/2:
                keepline = line
                keepindex=index+offset

                #self.screen.addstr(index+offset, 0, line, curses.A_BOLD)
                #td = len(line)
        self.screen.refresh()
        words = keepline.split()
        carriage = 0
        for i, word in enumerate(words):
            time.sleep(.2)
            if (carriage + len(word) + 1) < self.COLS:
                self.screen.addstr(keepindex, carriage, word, curses.A_BOLD)
            else:
                pass
            carriage += len(word)+1
            self.screen.refresh()

       

        return td

    # move highlight up/down one line
    def updown(self, increment):
        nextLineNum = self.highlightLineNum + increment
        self.topLineNum = self.highlightLineNum - curses.LINES/2 
        self.highlightLineNum = nextLineNum        
 
    def restoreScreen(self):
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    
    # catch any weird termination situations
    def __del__(self):
        self.restoreScreen()

     
if __name__ == '__main__':
    ih = MenuDemo()
    
