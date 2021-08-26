from FindIDWindow_ui import Ui_IDFindWindow
from PyQt5.QtWidgets import QDialog


class FindIDWIndow(QDialog, Ui_IDFindWindow):
    def __init__(self, parent, IDList):
        super().__init__(parent)
        self.setupUi(self)
        for i in IDList:
            self.listWidgetIDs.addItem(i)
        self.selectedID = ''
        self.buttonBox.accepted.connect(self.selectID)

    def selectID(self):
        if self.listWidgetIDs.currentItem():
            self.selectedID = self.listWidgetIDs.currentItem().text()
