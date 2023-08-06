#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 21:43:18 2020

@author: corkep
"""
import sys

try:
    from colored import fg, bg, attr
    _colored = True
    # print('using colored output')
except ImportError:
    # print('colored not found')
    _colored = False


class Column():
    def __init__(self, name, fmt="{}", width=None,
        colcolor=None, colbgcolor=None, colstyle=None, colalign=">", 
        headcolor=None, headbgcolor=None, headstyle=None, headalign=">"
        ):

        self.name = name
        self.fmt = fmt
        self.formatted = []
        self.fgcolor = []
        self.table = None

        if headalign is None:
            self.headalign = colalign
        self.colcolor = colcolor
        self.colbgcolor = colbgcolor
        self.colstyle = colstyle
        self.colalign = colalign

        self.headcolor = headcolor
        self.headbgcolor = headbgcolor
        self.headstyle = headstyle
        self.headalign = headalign

        self.width = width
        self.maxwidth = len(name)

    def _settyle(self, header):
        if header:
            color = self.headcolor
            bgcolor = self.headbgcolor
            style = self.headstyle
        else:
            color = self.colcolor
            bgcolor = self.colbgcolor
            style = self.colstyle

        text = ""
        if color is not None:
            text += self.table.FG(color)
        if bgcolor is not None:
            text += self.table.BG(bgcolor)
        if style is not None:
            text += self.table.ATTR(styledict[style])
        return text

def _spaces(n):
    return " " * n

def _aligntext(opt, text, n, color=None):
    gap = n - len(text)
    if color:
        # text = FG(color) + text + ATTR(0)
        text = color[0] + text + color[1]
    if  opt == '<':
        return text + _spaces(gap)
    elif opt == '>':
        return _spaces(gap) + text
    elif opt == '^':
        g1 = gap // 2
        g2 = gap - g1
        return _spaces(g1) + text + _spaces(g2)

#       ascii, thin, thin+round, thick, double
_tl = [ord('+'), 0x250c, 0x256d, 0x250f, 0x2554]
_tr = [ord('+'), 0x2510, 0x256e, 0x2513, 0x2557]
_bl = [ord('+'), 0x2514, 0x2570, 0x2517, 0x255a]
_br = [ord('+'), 0x2518, 0x256f, 0x251b, 0x255c]
_lj = [ord('+'), 0x251c, 0x251c, 0x2523, 0x2560]
_rj = [ord('+'), 0x2524, 0x2524, 0x252b, 0x2563]
_tj = [ord('+'), 0x252c, 0x252c, 0x2533, 0x2566]
_bj = [ord('+'), 0x2534, 0x2534, 0x253b, 0x2569]
_xj = [ord('+'), 0x253c, 0x253c, 0x254b, 0x256c]
_hl = [ord('-'), 0x2500, 0x2500, 0x2501, 0x2550]
_vl = [ord('|'), 0x2502, 0x2502, 0x2503, 0x2551]

borderdict = {"ascii": 0, "thin": 1, "round": 2, "thick": 3, "double": 4, "thick-thin": 5, "double-thin":6}
styledict = {"bold": 1, "dim": 2, "underlined": 4, "blink": 5, "reverse":7}

class ANSIMatrix:

    def __init__(self, style='thin', fmt='{:< 10.3g}', squish=True, squishtol=100):

        import numpy as np  # only import if matrix is used
        self.style = borderdict[style]
        self.fmt = fmt
        self.width = len(fmt.format(1))
        if squish:
            self.squish = squishtol * np.finfo(float).eps
        else:
            self.squish = None

    def str(self, matrix, suffix_super='', suffix_sub=''):

        import numpy as np  # only import if matrix is used

        if len(matrix.shape) == 1:
            ncols = matrix.shape[0]
            matrix = matrix.reshape((1, -1))
        elif len(matrix.shape) == 2:
            ncols = matrix.shape[1]
        else:
            raise ValueError('Only 1D and 2D arrays supported')

        mwidth = ncols * self.width + (ncols - 1)
        if self.squish is None:
            m2 = matrix
        else:
            m2 = np.where(abs(matrix) < self.squish, 0, matrix)
        b = self.style

        s = chr(_tl[b]) + ' ' * mwidth + chr(_tr[b]) + suffix_super + '\n'
        for row in m2:
            s += chr(_vl[b]) + ' '.join([self.fmt.format(x) for x in row]) + chr(_vl[b]) + '\n'
        s += chr(_bl[b]) + ' ' * mwidth + chr(_br[b]) + suffix_sub
        return s

    def print(self, matrix, *pos, file=sys.stdout, **kwargs):
        print(self.str(matrix, *pos, **kwargs), file=file)

class ANSITable:
    _color = _colored

    def __init__(self, *pos, colsep = 2, offset=0, border=None, bordercolor=None, ellipsis=True, columns=None, header=True, color=True):
 
        self.colsep = colsep
        self.offset = offset
        self.ellipsis = ellipsis
        self.rows = []
        self.bordercolor = bordercolor
        self.header = header
        self.color = color and self._color

        if border is not None:
            # printing borderes, adjust some other parameters
            if self.offset == 0:
                self.offset = 1
            self.colsep |= 1  # make it odd

            self.border = borderdict[border]
        else:
            self.border = None
        
        self.nrows = 0
        self.columns = []
        for c in pos:
            if isinstance(c, str):
                c = Column(c)
                c.table = self
                self.columns.append(c)
            elif isinstance(c, Column):
                c.table = self
                self.columns.append(c)
            else:
                raise TypeError('expecting a lists of Column objects')
        if len(self.columns) == 0 and columns is not None:
            for _ in range(columns):
                self.columns.append("")

    def addcolumn(self, name, **kwargs):
        self.columns.append(Column(name, **kwargs))

    def row(self, *values):
        assert len(values) == len(self.columns), 'wrong number of data items added'

        for value, c in zip(values, self.columns):
            if c.fmt is None:
                s = value
            elif isinstance(c.fmt, str):
                s = c.fmt.format(value)
            elif callable(c.fmt):
                s = c.fmt(value)
            else:
                raise ValueError('fmt must be valid format string or callable')

            # handle a FG color specifier
            if s.startswith('<<'):
                # color specifier is given
                end = s.find('>>')
                color = s[2:end]
                s = s[end+2:]
            else:
                color = None

            if c.width is not None and len(s) > c.width:
                if self.ellipsis:
                    s = s[:c.width - 1] + "\u2026"
                else:
                    s = s[:c.width]
            c.maxwidth = max(c.maxwidth, len(s))

            c.formatted.append(s)
            c.fgcolor.append(color)
        self.nrows += 1
                    
    def _topline(self):
        return self._line(_tl, _tj, _tr)

    def _midline(self):
        return self._line(_lj, _xj, _rj)

    def _bottomline(self):
        return self._line(_bl, _bj, _br)

    def _line(self, left, mid, right):
        if self.border is  None:
            return ""
        else:
            b = self.border
            c2 = self.colsep // 2
            text = _spaces(self.offset - 1)
            if self.bordercolor is not None:
                text += self.FG(self.bordercolor)
            text += chr(left[b])
            for c in self.columns:
                text += chr(_hl[b]) * (c.width + c2)
                if not c.last:
                    text += chr(mid[b]) + chr(_hl[b]) * c2 
            text += chr(right[b])
            if self.bordercolor is not None:
                text += self.ATTR(0)
            return text + "\n"

    def _vline(self):
        if self.border is not None:
            text = ""
            b = self.border
            if self.bordercolor is not None:
                text += self.FG(self.bordercolor)
            text += chr(_vl[b])
            if self.bordercolor is not None:
                text += self.ATTR(0)
            return text


    def _row(self, row=None):
        if self.border is not None:
            text = _spaces(self.offset - 1) + self._vline()
            for c in self.columns:

                ansi = c._settyle(row is None)
                text += ansi
                if row is None:
                    # header
                    text += _aligntext(c.headalign, c.name, c.width)
                else:
                    # table row proper
                    text += _aligntext(c.colalign, c.formatted[row], c.width, 
                        (self.FG(c.fgcolor[row]), self.ATTR(0)))
                if len(ansi) > 0:
                    text += self.ATTR(0)

                c2 = self.colsep // 2
                if not c.last:
                    text += _spaces(c2) + self._vline() +  _spaces(c2)
                else:
                    text += _spaces(c2) + self._vline()
        else:
            # no border
            text = _spaces(self.offset)

            for c in self.columns:
                ansi = c._settyle(row is None)
                text += ansi
                if row is None:
                    # header
                    text += _aligntext(c.headalign, c.name, c.width)
                else:
                    # table row proper
                    text += _aligntext(c.colalign, c.formatted[row], c.width, 
                                (self.FG(c.fgcolor[row]), self.ATTR(0)))
                if len(ansi) > 0:
                    text += self.ATTR(0)
                text +=  _spaces(self.colsep)

        return text + "\n"

    def print(self, file=None):
        if file is None:
            self.file = sys.stdout
        else:
            self.file = file

        print(str(self))

    def __str__(self):

        for i, c in enumerate(self.columns):
            c.width = c.width or c.maxwidth
            c.last = i == len(self.columns) - 1

        text = ""

        # heading
        text += self._topline()
        if self.header:
            text += self._row()
            text += self._midline()

        # rows

        for i in range(self.nrows):
            text += self._row(i)
        
        # footer
        text += self._bottomline()

        return text

    def FG(self, c):
        if self.color and c is not None:
            return fg(c)
        else:
            return ""

    def BG(self, c):
        if self.color and c is not None:
            return bg(c)
        else:
            return ""

    def ATTR(self, c):
        if self.color and c is not None:
            return attr(c)
        else:
            return "" 

if __name__ == "__main__":

    import numpy as np

    m = np.random.rand(4,4) - 0.5
    m[0,0] = 1.23456e-14
    print(m)
    print(np.array2string(m))

    formatter = ANSIMatrix(style='thick', squish=True)

    formatter.print(m)

    formatter.print(m, suffix_super='T', suffix_sub='3')

    m = np.random.rand(4) - 0.5
    formatter.print(m, 'T')

    
    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable("col1", "column 2 has a big header", "column 3", color=False)
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("<<red>>bbbbbbbbbbbbb", 5.5, 6)
    table.row("<<blue>>ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3")
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header", "{:.3g}"),
        Column("column 3", "{:-10.4f}")
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1", width=10),
        Column("column 2 has a big header", "{:.3g}"),
        Column("column 3", "{:-10.4f}")
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="ascii"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="thick"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header", colalign="^"),
        Column("column 3"),
        border="thick"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1", headalign="<"),
        Column("column 2 has a big header", colalign="^"),
        Column("column 3", colalign="<"),
        border="thick"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1", headalign="<"),
        Column("column 2 has a big header", colalign="^", colstyle="reverse"),
        Column("column 3", colalign="<"),
        border="thick"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1", headalign="<", colcolor="red", headstyle="underlined"),
        Column("column 2 has a big header", colalign="^", colstyle="reverse"),
        Column("column 3", colalign="<", colbgcolor="green", fmt="{: d}"),
        border="thick", bordercolor="blue"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()
