from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from ui_giris import Ui_MainWindow
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.toMainWindow)

    def toMainWindow(self):
        from main import MainWindow
        self.mainWindow = MainWindow()
        self.destroy(destroyWindow=True)





if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    loginWindow = MainWindow()
    loginWindow.show()
    sys.exit(app.exec_())
