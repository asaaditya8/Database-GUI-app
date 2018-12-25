import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

import DB_manager


class App(QtWidgets.QWidget):
    """docstring for App"""

    def __init__(self, database, tableName):
        super(App, self).__init__()
        uic.loadUi('entry.ui', self)
        self.setWindowTitle('APP Pyqt Gui')
        self.dbu = database
        self.tableName = tableName

        self.inputs = {'fname': self.fnameLineEdit,
                       'mname': self.mnameLineEdit,
                       'lname': self.lnameLineEdit,
                       'sex': self.sexComboBox,
                       'age': self.ageSpinBox
                       }

        self.inputs['sex'].addItems(['M', 'F'])
        # self.inputs['sex'].currentIndexChanged.connect(self.selectionchange)
        self.submitPushButton.clicked.connect(self.Commit)
        self.treeWidget.itemClicked.connect(self.printin)

        self.worke = DB_handler(db=self.dbu, tableName=self.tableName)
        self.worke.result.connect(self.UpdateTree)
        self.worke.finished.connect(self.enableSubmitButton)

        self.submitPushButton.setEnabled(False)
        self.worke.start()

    # @pyqtSlot()
    # def selectionchange(self):
    #     print(self.inputs['sex'].currentText())
    @pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def printin(self, item, col):
        print(item.text(0))

    @pyqtSlot()
    def enableSubmitButton(self):
        self.submitPushButton.setEnabled(True)

    @pyqtSlot()
    def Commit(self):
        self.submitPushButton.setEnabled(False)
        fname = self.inputs['fname'].text()
        mname = self.inputs['mname'].text()
        lname = self.inputs['lname'].text()
        sex = self.inputs['sex'].currentText()
        age = self.inputs['age'].value()
        self.dbu.AddRecordToTable(self.tableName, (fname, mname, lname, sex, age))
        self.worke.start()

    @pyqtSlot(list, list)
    def UpdateTree(self, col, table):

        for c in range(len(col)):
            self.treeWidget.headerItem().setText(c, col[c][0])

        self.treeWidget.clear()

        for item in range(len(table)):
            QtWidgets.QTreeWidgetItem(self.treeWidget)
            for value in range(len(table[item])):
                self.treeWidget.topLevelItem(item).setText(value, str(table[item][value]))


class DB_handler(QThread):
    result = pyqtSignal(list, list)
    finished = pyqtSignal()

    def __init__(self, parent=None, db=None, tableName=None):
        super(DB_handler, self).__init__(parent)
        self.db = db
        self.tableName = tableName

    def run(self):
        col = self.db.GetColumns(self.tableName)
        table = self.db.GetTable(self.tableName)
        self.finished.emit()
        self.result.emit(col, table)

if __name__ == '__main__':

    db = 'patient_try'
    tableName = 'patient'
    dbu = DB_manager.DatabaseUtility(db)
    app = QtWidgets.QApplication(sys.argv)
    widget = App(dbu, tableName)
    widget.show()
    sys.exit(app.exec_())