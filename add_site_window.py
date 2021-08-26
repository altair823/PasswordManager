from AddSiteWindow_ui import Ui_AddSiteWindow
from PyQt5.QtWidgets import QDialog


class AddSiteWindow(QDialog, Ui_AddSiteWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.inputSiteName)
        self.buttonBox.rejected.connect(self.cancel)

    def inputSiteName(self):
        self.newSiteName = self.lineEditSiteName.text()
        self.close()

    def cancel(self):
        self.newSiteName = None
        self.close()
