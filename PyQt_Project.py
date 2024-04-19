from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QMessageBox, QWidget
from math import sqrt
import sqlite3
import sys
import numpy as np
import matplotlib.pyplot as plt
from random import choice
from PIL import Image


class Project(QMainWindow):  # основа программы
    def __init__(self):
        super(Project, self).__init__()
        self.setMinimumHeight(500)
        self.setMinimumWidth(600)
        self.setMaximumHeight(500)
        self.setMaximumWidth(600)
        self.setFixedHeight(500)
        self.setFixedWidth(600)
        self.line = QLabel(self)
        self.line.setFixedWidth(600)
        self.line.setFixedHeight(500)
        self.line.setMaximumWidth(600)
        self.line.setMaximumHeight(500)
        self.setWindowTitle("Решатор квадратных уравнений")

        self.l1 = QtWidgets.QLabel(self)
        self.l1.setGeometry(QtCore.QRect(5, 10, 590, 31))

        self.l1.setText("Введите коэффициенты квадратного уравнения:")

        self.e1 = QtWidgets.QLineEdit('2', self)
        self.e1.setGeometry(QtCore.QRect(59, 60, 27, 31))

        self.l2 = QtWidgets.QLabel(self)
        self.l2.setGeometry(QtCore.QRect(90, 60, 565, 31))
        self.l2.setText("x² +")

        self.e2 = QtWidgets.QLineEdit('7', self)
        self.e2.setGeometry(QtCore.QRect(120, 60, 37, 31))
        self.e2.setObjectName("e2")

        self.l3 = QtWidgets.QLabel(self)
        self.l3.setGeometry(QtCore.QRect(156, 60, 31, 31))
        self.l3.setObjectName("l3")
        self.l3.setText("x +")

        self.e3 = QtWidgets.QLineEdit('3', self)
        self.e3.setGeometry(QtCore.QRect(180, 60, 31, 31))
        self.e3.setObjectName("e3")

        self.l4 = QtWidgets.QLabel(self)
        self.l4.setGeometry(QtCore.QRect(210, 60, 31, 31))
        self.l4.setObjectName("l4")
        self.l4.setText("=")

        self.e4 = QtWidgets.QLineEdit('0', self)
        self.e4.setEnabled(False)
        self.e4.setGeometry(QtCore.QRect(230, 60, 31, 31))
        self.e4.setObjectName("e4")

        self.btn = QtWidgets.QPushButton(self)
        self.btn.setObjectName("btn")
        self.btn.setGeometry(QtCore.QRect(10, 100, 285, 25))
        self.grafic = QtWidgets.QPushButton(self)
        self.grafic.setObjectName("grafic")
        self.grafic.setGeometry(QtCore.QRect(285, 100, 300, 25))
        self.grafic.setText("Показать график уравнения")
        self.btn.setText("Решить уравнение")
        self.btn.clicked.connect(self.reshenye)
        self.grafic.clicked.connect(self.plot_equation)

        self.textEdit = QtWidgets.QTextBrowser(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 140, 580, 350))
        self.textEdit.setObjectName("textEdit")

        self.e1.setPlaceholderText("a")
        self.e2.setPlaceholderText("b")
        self.e3.setPlaceholderText("c")
        self.e4.setPlaceholderText("d")

    def plot_equation(self):  # cоздание графика
        a = float(self.e1.text())
        b = float(self.e2.text())
        c = float(self.e3.text())

        x = np.linspace(-10, 10, 100)
        y = a * x ** 2 + b * x + c

        plt.plot(x, y)
        plt.xlabel('x (ось абсцисс)')
        plt.ylabel('y (ось ординат)')
        plt.title(f'График квадратного уравнения {self.e1.text()}x² + {self.e2.text()}x + {self.e3.text()} = 0')
        plt.grid(True)
        if self.diskriminant >= 0:
            plt.show()

    def reshenye(self):  # решение уравнений
        a = self.e1.text()
        b = self.e2.text()
        c = self.e3.text()
        d = self.e4.text()
        val_c = float(c) - float(d)  # с, если уравнение равняется 0
        self.diskriminant = float(b) * float(b) - (4 * float(a) * float(val_c))  # Дискриминант
        global x1, x2, x3
        if self.diskriminant > 0:
            x1 = (sqrt(self.diskriminant) - float(b)) / (2 * float(a))
            x2 = (-sqrt(self.diskriminant) - float(b)) / (2 * float(a))
            self.textEdit.setText(
                f'Дискриминант квадратного уравнения равен {str(self.diskriminant).replace(".", ",")}. Квадратное уравнение имеет решение в виде двух значений аргумента x. X1 = {str(x1).replace(".", ",")}. X2 = {str(x2).replace(".", ",")}. ')
        elif self.diskriminant < 0:
            self.textEdit.setText(
                f'Дискриминант квадратного уравнения равен {str(self.diskriminant).replace(".", ",")}. Уравнение не имеет корней.')

        elif self.diskriminant == 0:
            x3 = -float(b) / (2 * float(a))
            self.textEdit.setText(
                f'Дискриминант квадратного уравнения равен {str(self.diskriminant).replace(".", ",")}. Квадратное уравнение имеет решение в виде одного значения аргумента x. X = {str(x3).replace(".", ",")}. ')


class DatabaseManager:  # подключение базы данных
    def __init__(self):
        self.connection = sqlite3.connect("Project.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS uravneniya (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")

    def insert_user(self, name):
        self.cursor.execute("INSERT INTO uravneniya (name) VALUES (?)", (name,))
        self.connection.commit()

    def get_users(self):
        self.cursor.execute("SELECT * FROM uravneniya")
        return self.cursor.fetchall()


class dobav_urav(QWidget):  # меню работы с базой данных
    def __init__(self, db_manager):
        self.db_manager = db_manager
        super().__init__()
        self.layout = QVBoxLayout()
        self.name_label = QLabel("Введите уравнение ↓")
        self.name_input = QLineEdit('2x² + 7x + 3 = 0', self)
        self.dobav_button = QPushButton("Добавить в базу данных")
        self.dobav_button.clicked.connect(self.proverka_na_nalichie)
        self.dobav_urav = QPushButton('Брат накинь уравнение по брацки')
        self.dobav_urav.clicked.connect(self.nakin_urav)
        self.pict = QPushButton('цель')
        self.pict.clicked.connect(self.picture)
        self.mem = QPushButton('Мем чтобы не грустить')
        self.mem.clicked.connect(self.meem)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.dobav_button)
        self.layout.addWidget(self.dobav_urav)
        self.layout.addWidget(self.pict)
        self.layout.addWidget(self.mem)
        self.setLayout(self.layout)

    def picture(self):
        a = ['car2.png', 'car1.jpg', '1qw.jpg', '2qw.jpg', '5mem.jpg']
        image = Image.open(choice(a))
        image.show()

    def meem(self):
        b = ['1mem.jpg', '2mem.jpg', '3mem.jpg', '4mem.jpg', '3qw.png']
        im = Image.open(choice(b))
        im.show()

    def nakin_urav(self):
        QMessageBox.information(self, "Конечно брат всё для тебя", "Уравнение введено в строку")
        a = choice(range(2, 10))
        b = choice(range(-100, 100))
        c = choice(range(-100, 100))
        if b > 0 and c > 0:
            self.name_input.setText(f'{a}x² + {b}x + {c} = 0')
        elif b > 0 > c:
            self.name_input.setText(f'{a}x² + {b}x {c} = 0')
        elif c > 0 > b:
            self.name_input.setText(f'{a}x² {b}x + {c} = 0')
        else:
            self.name_input.setText(f'{a}x² {b}x {c} = 0')

    def proverka_na_nalichie(self):
        name = self.name_input.text()
        if name:
            self.db_manager.insert_user(name)
            QMessageBox.information(self, "Красавчик брат твоё моё и всё", "Уравнение добавлено в базу данных")
            self.name_input.clear()
        else:
            QMessageBox.warning(self, "Эээ брат, чо как лох?", "Коэффициенты введи")


class Uravlist(QWidget):  # виджет на котором база
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Решатор уравнений :)")
        self.layout = QVBoxLayout()
        self.users_label = QLabel("Уравнения")
        self.user_list_label = QLabel()
        self.layout.addWidget(self.users_label)
        self.layout.addWidget(self.user_list_label)
        self.setLayout(self.layout)

    def dobav_uravneniya_v_list(self):
        users = self.db_manager.get_users()
        user_list_text = ""
        for user in users:
            user_list_text += f"{user[0]}. {user[1]}\n"
        self.user_list_label.setText(user_list_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    urav_window = dobav_urav(db_manager)
    urav_list_window = Uravlist(db_manager)
    urav_window.dobav_button.clicked.connect(urav_list_window.dobav_uravneniya_v_list)
    main_layout = QHBoxLayout()
    main_layout.addWidget(urav_window)
    main_layout.addWidget(urav_list_window)
    main_widget = QWidget()
    main_widget.setLayout(main_layout)
    main_widget.setGeometry(245, 260, 415, 160)
    form = Project()
    form.show()
    main_widget.show()
    sys.exit(app.exec_())
