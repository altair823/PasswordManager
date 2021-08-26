from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())