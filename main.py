class bol():
    def __init__(self, x):
        self.x = x
        if type(x) == str:
            if x == 'True':
                self.x = True
            elif x == 'False':
                self.x = False
            else:
                #print(x, type(x))
                global namedict
                #print(namedict[x])
                self.x = result(x) #namedict[x]


    def __eq__(self, other):
        if type(other) == str:
            other = result(other)
        if type(other) == type(bol(True)):
            other = other.res()
        return self.x == other


    def __add__(self, other):
        if type(other) == str:
            other = result(other)
        if type(other) == type(bol(True)):
            other = other.res()
        return self.x or other


    def __sub__(self, other):
        if type(other) == str:
            other = result(other)
        if type(other) == type(bol(True)):
            other = other.res()
        return  self.x and other


    def __mul__(self, other):
        if type(other) == str:
            other = result(other)
        if type(other) == type(bol(True)):
            other = other.res()
        return self.x and not other


    def __mod__(self, other):
        if type(other) == str:
            other = result(other)
        if type(other) == type(bol(True)):
            other = other.res()
        return self.x != other


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


def result(x):
    global namedict
    #print(x)
    return namedict[x]

def prov_bool_list(a):
    if len(a) == 0:
        return True
    else:
        for i in range(1, len(a)):
            if a[i] != a[i - 1]:
                return False
        return True

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
    znak = {'∪': '+', '⋂': '-', "\\": '*', '*': '/'}
    znak = {'∪': '+', '⋂': '-', "\\": '*', 'Δ': '%', '∅': 'False'}
    a = s.split('=')
    split_list = ['+', '-', '*', ' ', '(', ')', '=', '%']
    if len(a) > 1:
        try:
            s1 = ''
            for i in s:
                s1 += znak.get(i, i)
                if i == '=':
                    s1 += '='
            name, s1 = split(s1, split_list)
            name = list(set(name))
            print(name)
            s1 = bolname(s1, name)
            c = True
            global dv
            dv = []
            f([], len(name))
            print(len(name))
            global names_var
            names_var = name
            global res_list_base
            print(s, s1)
            for i in dv:
                namedict = dict()
                for k in range(len(name)):
                    namedict[name[k]] = i[k]
                #print(s1)
                #print(name)
                #print(i)
                #print(namedict)
                try:
                    bool_res_list = list(map(lambda x: bool(eval(x)), s1.split('==')))
                    bool_res = prov_bool_list(bool_res_list)
                    #print(bool_res == eval(s1), 5)
                    #bool_res = eval(s1)
                    res_list_base.append(i + bool_res_list + [bool_res])
                    if not bool_res:
                        c = False
                except:
                    c = False
                    return 'Ошибка расчёта'
            name += a
            return c
        except:
            s1 = ''
            for i in s:
                s1 += znak.get(i, i)
                if i == '=':
                    s1 += '='
            name, s1 = split(s1, split_list)
            name = list(set(name))
            if 'bol' in name:
                return 'В вражении нельзя испольовать имя bol'
            else:
                return 'Некорректное выражения'
    else:
        return 'Ошибка количества выражений'


def main():
    return provset(input('Введите, пожалуйста выражение с использованием операторов ∪ или +, ⋂ или -, \\ или * '))


class File:
    def __init__(self, name):
        self.name = name + '.db'

    def save(self, s, answer, name_table, name_list, res):
        print(self.name)
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        n = len(name_list) + 1
        sql = 'CREATE TABLE IF NOT EXISTS'
        cursor.execute( 'Drop table if exists ' + name_table) #удалеиние таблицы
        sql += ' ' + name_table + '('
        for i in range(n):
            if i == n - 1:
                sql += 'atr' + str(i) + ' ' + 'text'
            else:
                sql += 'atr' + str(i) + ' ' + 'text' + ','
        sql += ');'
        #sql += '/n' + s + ' = ' + str(answer)
        print(sql)
        cursor.execute(sql)
        #wprint(cursor.fetchall())  # o
        sql = 'INSERT INTO ' + name_table + ' VALUES('
        for i in name_list:
            sql += '"' + str(i) + '"' + ','
        sql += '"result=' + str(answer) + '")'
        #print(sql)
        cursor.execute(sql)
        for i in res:
            sql = 'INSERT INTO ' + name_table + ' VALUES('
            for j in range(len(i)):
                if j == len(i) - 1:
                    sql += '"' + str(i[j]) + '"' + ')'
                else:
                    sql += '"' + str(i[j]) + '"' + ','
            #print(sql)
            cursor.execute(sql)
        conn.commit()
        #Drop table if exists
        #CREATE TABLE IF NOT EXISTS

def get_string_ex(s):
    #функция котрая получает пременную и вовразает строку где записаны предки класас этой перееменнойй через точку
    s = type(s).__bases__
    s = str(s)
    return s.split("'")[1]

def get_ex(a, prov):
    #функция которая проверяет есть ли предок prov
    s = get_string_ex(a)
    s = s.split('.')
    return prov in s


import sys
from decimal import Decimal
import sqlite3
#import base_data

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import base_to_pdf
import os


class Menu(QWidget):
    #resized = QtCore.pyqtSignal()


    def __init__(self, name_table_main):
        super().__init__()
        self.n = 3
        self.Widgets = []
        self.setWindowTitle("Калькулятор")
        self.delta = 0.00000001
        self.setGeometry(600, 300, 240 * self.n, 330)
        font = QFont()
        font.setPointSize(30)
        self.dict_cor_size = dict()
        self.main = QLineEdit('', self)
        self.main.setGeometry(0, 15, 239 * self.n, 60)
        self.main.setFont(font)
        self.main.setAlignment(QtCore.Qt.AlignRight)
        self.Widgets.append(self.main)
        self.result = QLabel('', self)
        self.result.setGeometry(0, 0, 238 * self.n, 15)
        self.result.setAlignment(QtCore.Qt.AlignRight)
        #znak = {'∪': '+', '⋂': '-', "\\": '*', '*': '//'}
        self.Widgets.append(self.result)
        #self.resized.connect(self.someFunction)
        symbols = ['A', 'B', 'C', 'Δ',
                   'D', 'F', 'K', '\\',
                   'L', 'M', '∅', '⋂',
                   '<-', '=', 'CE', '∪',
                   '(', ')', 'prov']
        #self.spec_symbols = znak.keys()+
        self.btns = []
        v_size, h_size = 50, 60 * self.n
        for i in range(0, h_size * len(symbols), h_size):
            btn = QPushButton(symbols[i // h_size], self)
            btn.setGeometry(i % (h_size * 4), 80 + v_size * (i // (h_size * 4)), h_size, v_size)
            btn.clicked.connect(self.btn_pressed)
            self.btns.append(btn)
        self.btns[-1].resize(120 * self.n, 50)
        self.Widgets += self.btns

        self.main_text, self.result_text, self.last_sender = '', '', ''
        self.file = File(name_table_main + '.db')
        for  i in self.Widgets:
            self.dict_cor_size[i] = [i.pos().x(), i.pos().y(), i.size().width(), i.size().height()]

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
        global name_table_main
        ev_str = self.main_text
        self.file.name = name_table_main + '.db'
        if ev_str[-2:] == '/0':
            res_text = "ОШИБКА"
        else:
            global res_list_base
            global names_var
            res_list_base = []
            names_var = []
            res_text = str(provset(ev_str))
        self.result_text = str(res_text)
        if self.result_text in ['True', 'False']:
            self.result.setStyleSheet("QLabel {color:black}")
        else:
            self.result.setStyleSheet("QLabel {color:red}")
        self.result.setText(self.result_text)
        if self.result_text in ['True', 'False']:
            self.file.save(self.main_text, self.result_text, 'name_table1', names_var, res_list_base)
            try:
                base_to_pdf.table_to_docx(self.file.name, 'name_table1', self.main_text, self.result_text)
            except:
                try:
                    import os
                    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ''.join(name_table_main.split('.')[:-1]) + ".docx")
                    os.remove(path)
                except:
                    self.result_text += ' Файл не верный!'
                    self.result.setText(self.result_text)
                    self.result.setStyleSheet("QLabel {color:red}")


    '''
    def resizeEvent(self, event):
        self.resized.emit()
        return super(Menu, self).resizeEvent(event)

    def someFunction(self):
        for i in self.Widgets:
            if True:
                a = self.dict_cor_size[i]
                width = self.size().width()
                height = self.size().height()
                koefW = width / self.w
                koefH = height / self.h
                i.setGeometry(a[0] * koefW, a[1] * koefH, a[2] * koefW, a[3] * koefH)
                #self.__setattr__(i, b)
    '''

class Table(QWidget):
    def __init__(self, file_name, table_name):
        super().__init__()
        self.n = 3
        self.setWindowTitle("Калькулятор")
        self.delta = 0.00000001
        conn = sqlite3.connect(file_name)
        cursor = conn.cursor()
        sql = 'select count(*) from ' + table_name
        cursor.execute(sql)
        sql = 'select count(*) from pragma_table_info("' + table_name + '")'
        n = cursor.fetchone()
        cursor.execute(sql)
        m = cursor.fetchone()
        central_widget = QWidget(self)  # Создаём центральный виджет
        print('443')
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
        print('443')
        #self.setCentralWidget(central_widget)
        print('442')
          # Создаём QGridLayout
        table = QTableWidget(self)
        table.setColumnCount(int(m[0]))  # Устанавливаем три колонки
        table.setRowCount(int(n[0]))
        sql = 'SELECT * FROM ' + table_name
        cursor.execute(sql)
        a = cursor.fetchall()
        print(a, n[0], m[0])
        for i in range(len(a)):
            x = list(a[i])
            for j in range(len(x)):
                table.setItem(i, j, QTableWidgetItem(str(a[i][j])))
        grid_layout.addWidget(table, 0, 0)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        global name_table_main
        self.n = 3
        self.setWindowTitle("Калькулятор")
        self.delta = 0.00000001
        self.setGeometry(600, 300, 240 * self.n, 330)
        font = QFont()
        font.setPointSize(30)
        self.main = QLineEdit('', self)
        self.main.setGeometry(0, 250, 239 * self.n - 60, 60)
        self.main.setFont(font)
        btn = QPushButton('Далее', self)
        btn.setGeometry(239* self.n + 1 - 60, 250, 60, 60)
        btn.clicked.connect(self.btn_pressed)
        #self.main_file = QLineEdit('', self)
        #self.main_file.setGeometry(0, 180, 239 * self.n - 60, 60)
        #self.main.setFont(font)
        #btn_file = QPushButton('Далее', self)
        #btn_file.setGeometry(239 * self.n + 1 - 60, 180, 60, 60)
        #btn_file.clicked.connect(self.btn_file_pressed)

        self.result = QLabel('', self)
        self.result.setGeometry(0, 0, 238 * self.n, 15)
        self.result.setAlignment(QtCore.Qt.AlignRight)

    def btn_file_pressed(self):
        try:
            s = self.main_file.text()
            s = s.split(';')
            s[0] = ''.join(s[0].split())
            s[1] = ''.join(s[1].split())
            #QtWidgets.QFileDialog.getOpenFileName()
            #name.db;name_table1
            app_table= QApplication(sys.argv)

            form_main = Table(s[0], s[1])
            print(2)
            form_main.show()
            app_table.exec()

        except:
            print(55555)
            self.result.text = 'Файл не найден'
            self.result.setStyleSheet("QLabel {color:red}")

    def btn_pressed(self):
        global name_table_main
        sender = self.sender().text()
        self.main_text = self.main.text()
        name_table_main = self.main_text
        c = False
        if name_table_main == '':
            result_text = 'Введено пустое имя'
        elif '.' in name_table_main:
            result_text = 'Введённое имя файла имеет тип'
        else:
            c = True
            result_text = 'Ведено всё верно'
        if c:
            self.result.setStyleSheet("QLabel {color:black}")
        else:
            self.result.setStyleSheet("QLabel {color:red}")
        self.result.setText(result_text)


if __name__ == '__main__':
    global name_table_main
    name_table_main = '5'
    app = QApplication(sys.argv)
    form = Menu(name_table_main)
    form.show()
    form_main = Main()
    form_main.show()
    sys.exit(app.exec())
