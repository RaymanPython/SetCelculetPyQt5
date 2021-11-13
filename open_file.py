import sys
from decimal import Decimal
import sqlite3
#import base_data

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets


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



if __name__ == '__main__':
    global name_table_main
    app = QApplication(sys.argv)
    form = Menu(name_table_main)
    form.show()
    sys.exit(app.exec())
