import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from PyQt6 import uic


class AddCoffee(QDialog):
    def __init__(self, parent=None, names=None):
        super().__init__(parent)
        self.re = ''
        self.names = names
        print(self.names)
        self.setWindowTitle('Add/edit coffee')
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.buttonBox.accepted.connect(self.save)

    def save(self):
        name = self.name.text()
        level = int(self.level.text())
        type = self.comboBox.currentText()
        desc = self.desc.text()
        price = int(self.price.text())
        v = float(self.volume.text())
        if name not in self.names:
            self.re = f"INSERT INTO Coffee VALUES (NULL, '{name}', {level}, '{type}', '{desc}', {price}, {v})"
        else:
            self.re = f"""UPDATE Coffee SET
                            level = {level},
                             type = '{type}',
                            description = '{desc}',
                            price = {price},
                            V = {v}
                            WHERE name = '{self.name.text()}'"""
        self.close()


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.setWindowTitle('Капучино')
        self.cur = self.con.cursor()
        self.loadtable()
        self.changebtn.clicked.connect(self.additem)

    def loadtable(self):
        res = self.cur.execute("SELECT * FROM Coffee").fetchall()

        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень прожарки', 'молотый/в зернах', 'описание вкуса', 'цена',
             'объем упаковки'])
        self.tableWidget.setRowCount(len(res))
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def additem(self):
        names = self.cur.execute("SELECT name FROM Coffee").fetchall()
        names = [i[0] for i in names]
        w = AddCoffee(parent=self, names=names)
        w.exec()
        if w.re != '':
            self.cur.execute(w.re)
            self.con.commit()
            self.loadtable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
