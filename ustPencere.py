import sys
from PyQt5.QtWidgets import QApplication, QTabBar, QMainWindow, QTabWidget, QWidget
import mainPencere


class ust_pencere(QMainWindow):

    def __init__(self):
        super(ust_pencere, self).__init__()

        self.tableriEkle()

    def tableriEkle(self):
        tabs = QTabWidget()
        tab_taks = QWidget()

        tabs.addTab(tab_taks)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ust_pencere_ins = ust_pencere()
    ust_pencere_ins.show()
    sys.exit(app.exec_())
