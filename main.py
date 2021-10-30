class bol():
    def __init__(self, x):
        self.x = x
        if type(x) == str:
            if x == 'True':
                self.x = True
            elif x == 'False':
                self.x = False
            else:
                self.x = res(x)


    def __eq__(self, other):
        if type(other) == str:
            other = res(other)
        if type(other) == type(bol(True)):
            other = other.res()
        return self.x == other


    def __add__(self, other):
        if type(other) == str:
            other = res(other)
        if type(other) == type(bol(True)):
            other = other.res()
        return self.x or other


    def __sub__(self, other):
        if type(other) == str:
            other = res(other)
        if type(other) == type(bol(True)):
            other = other.res()
        return  self.x and other


    def __mul__(self, other):
        if type(other) == str:
            other = res(other)
        if type(other) == type(bol(True)):
            other = other.res()
        return self.x and not other


    def __floordiv__(self, other):
        if type(other) == str:
            other = res(other)
        if type(other) == type(bol(True)):
            other = other.res()
        if self.x:
            return other
        else:
            return not other


    def res(self):
        return self.x



def bolname(s, name):
    s1 = ''
    c = True
    for i in s:
        if i == '(':
            s1 += 'bol'
        s1 += i
    return s1


def res(x):
    global namedict
    return namedict[x]


def split(s, b):
    a = []
    k = ''
    s1 = ''
    s = s + '*'
    c = True
    for i in s:
        if i not in b:
            k += i
            if c:
                s1 += '('
                c = False
        else:
            if k != '':
                s1 += "'" + k + "'"
                if k != 'True' and k != 'False':
                    a.append(k)
                k = ''
                if not c:
                    c = True
                    s1 += ')'
            s1 += i
    s1 = s1[0:-1]
    return a, s1


def f(a, n):
    global dv
    if n == 0:
        try:
            dv.append(a)
        except:
            dv = [a]
    else:
        f(a + [True], n - 1)
        f(a + [False], n - 1)


def provset(s):
    global namedict, dv

    a = s.split('=')
    znak = {'∪': '+', '⋂': '-', "\\": '*', 'Δ': '//', '∅':  'False'}
    if len(a) > 1:
        try:
            s1 = ''
            for i in s:
                s1 += znak.get(i, i)
                if i == '=':
                    s1 += '='
            name, s1 = split(s1, ['+', '-', '*', ' ', '(', ')', '=', '\\', '//'])
            name = list(set(name))
            s1 = bolname(s1, name)
            c = True
            global dv
            dv = []
            f([], len(name))
            for i in dv:
                namedict = dict()
                for k in range(len(name)):
                    namedict[name[k]] = i[k]
                print(s1)
                try:
                    if not eval(s1):
                        c = False
                        return c
                        break
                except:
                    c = False
                    return 'Ошибка расчёта'
            if c:
                return c
        except:
            s1 = ''
            for i in s:
                s1 += znak.get(i, i)
                if i == '=':
                    s1 += '='
            name, s1 = split(s1, ['+', '-', '*', ' ', '(', ')', '=', 'Δ', '∅'])
            name = list(set(name))
            if 'bol' in name:
                return 'В вражении нельзя испольовать имя bol'
            else:
                return 'Некоректное выражение'
    else:
        return 'Ошибка количества выражений'


import sys
from decimal import Decimal

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import *


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.n = 3
        self.setWindowTitle("Калькулятор")
        self.delta = 0.00000001
        self.setGeometry(600, 300, 240 * self.n, 330)
        font = QFont()
        font.setPointSize(30)
        self.main = QLineEdit('', self)
        self.main.setGeometry(0, 15, 239 * self.n, 60)
        self.main.setFont(font)
        self.main.setAlignment(QtCore.Qt.AlignRight)

        self.result = QLabel('', self)
        self.result.setGeometry(0, 0, 238 * self.n, 15)
        self.result.setAlignment(QtCore.Qt.AlignRight)
        #znak = {'∪': '+', '⋂': '-', "\\": '*', '*': '//'}
        symbols = ['A', 'B', 'C', 'Δ',
                   'D', 'F', 'K', '\\',
                   'L', 'M', '∅', '⋂',
                   '<-', '=', 'CE', '∪',
                   '(', ')', 'prov']
        #self.spec_symbols = znak.keys()
        self.btns = []

        v_size, h_size = 50, 60 * self.n
        for i in range(0, h_size * len(symbols), h_size):
            btn = QPushButton(symbols[i // h_size], self)
            btn.setGeometry(i % (h_size * 4), 80 + v_size * (i // (h_size * 4)), h_size, v_size)
            btn.clicked.connect(self.btn_pressed)
            self.btns.append(btn)
        self.btns[-1].resize(120 * self.n, 50)

        self.main_text, self.result_text, self.last_sender = '', '', ''

    def btn_pressed(self):
        sender = self.sender().text()
        self.main_text = self.main.text()
        if sender == 'CE':
            self.main_text = ''
        elif sender == 'prov':
            self.equal()
        elif sender == '<-':
            self.main_text = self.main_text[:-2]
        else:
            self.main_text += ' ' + sender
        self.main.setText(self.main_text)

    def equal(self):
        ev_str = self.main_text
        if ev_str[-2:] == '/0':
            res = "ОШИБКА"
        else:
            res = str(provset(ev_str))
        self.result_text = str(res)
        if self.result_text in ['True', 'False']:
            self.result.setStyleSheet("QLabel {color:black}")
        else:
            self.result.setStyleSheet("QLabel {color:red}")
        self.result.setText(self.result_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Menu()
    form.show()
    sys.exit(app.exec())
