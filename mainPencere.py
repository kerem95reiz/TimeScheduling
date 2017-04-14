import sys

from PyQt5 import QtGui

from bilgiGirrmeYeri import penceremiz
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QListView, \
    QAction, QListWidget, QListWidgetItem, QMessageBox, QProgressBar
import databaseConnection


class anaPencere(QMainWindow):
    def __init__(self):
        super(anaPencere, self).__init__()

        self.title = 'Yapilacaklar'
        self.xPos = 250
        self.yPos = 250
        self.width = 700
        self.height = 400
        self.pencereyi_olustur()

        # MENUBAR
        self.statusBar()

        mainMenu = self.menuBar()

        self.openTasksMenu = QAction("Tasks", self)
        self.openTasksMenu.setStatusTip("Taskleri acmak uzeresin")
        self.openTasksMenu.triggered.connect(self.openTasks)
        self.pencereler = mainMenu.addMenu('Pencereler')
        self.pencereler.addAction(self.openTasksMenu)

        self.openFinanceMenu = QAction("Financial", self)
        self.openFinanceMenu.setStatusTip("Finance bir goz at")
        self.openFinanceMenu.triggered.connect(self.openFinance)
        self.pencereler.addAction(self.openFinanceMenu)

        self.openGenerelMenu = QAction('Generel', self)
        self.openGenerelMenu.setStatusTip('Generele bir goz at')
        self.openGenerelMenu.triggered.connect(self.openGenerel)
        self.pencereler.addAction(self.openGenerelMenu)

    @pyqtSlot()
    def openTasks(self):
        print("Burada Tasks penceresini acacagiz")

    @pyqtSlot()
    def openFinance(self):
        print("Burada finance bir goz atacagiz, sonradan :D")

    @pyqtSlot()
    def openGenerel(self):
        print("Burada da Genel bi bakis acisi elde edevcegiz")


    def pencereyi_olustur(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.xPos, self.yPos, self.width, self.height)

        self.setCentralWidget(anaPencereIcerigi())


class anaPencereIcerigi(QWidget):
    def __init__(self):
        super(anaPencereIcerigi, self).__init__()
        self.pencereyi_olustur()

    def pencereyi_olustur(self):

        # BUTTONS
        self.gorevEkleButton = QPushButton('Ekle')
        self.gorevEkleButton.clicked.connect(self.task_ekle)

        self.yapilmislariGoruntule = QPushButton('Gecmis')
        self.yapilmislariGoruntule.clicked.connect(self.gecmis_taskleri_goruntule_alt)

        self.gorevleriYenile = QPushButton('Listeyi Guncelle')
        self.gorevleriYenile.clicked.connect(self.gecmis_taskleri_goruntule)

        self.programiKapat = QPushButton('Programi Sonlandir')
        self.programiKapat.clicked.connect(self.kapat)

        self.delete_item_from_list = QPushButton('Secilmisi Sil')
        self.delete_item_from_list.clicked.connect(self.secilmis_elemani_sil)

        #LIST
        self.tasks_list = QListWidget()
        # self.tasks_list.setModelColumn(3)
        self.tasks_list.doubleClicked.connect(self.listeye_tiklandi)

        #LAYOUT
        self.yanLayoutVB = QVBoxLayout()
        self.yanLayoutVB.addWidget(self.gorevEkleButton)
        self.yanLayoutVB.addWidget(self.yapilmislariGoruntule)
        self.yanLayoutVB.addWidget(self.gorevleriYenile)
        self.yanLayoutVB.addWidget(self.programiKapat)

        self.sagYandakiLayout = QVBoxLayout()
        self.sagYandakiLayout.addWidget(self.tasks_list, 9)
        self.sagYandakiLayout.addWidget(self.delete_item_from_list, 1)

        self.anaLayoutHB = QHBoxLayout()
        self.anaLayoutHB.addLayout(self.yanLayoutVB, 1)
        self.anaLayoutHB.addLayout(self.sagYandakiLayout, 7)

        self.setLayout(self.anaLayoutHB)

    def birFormat(self):
        dialog = self.numberformatdlg2.nu

    # METHODS

    @pyqtSlot()
    def gecmis_taskleri_goruntule(self):

        self.db_bag = databaseConnection.db_connect()
        self.tasks_list.clear()
        self.yapilacaklar_listesi = []
        self.yapilacaklar_listesi = self.db_bag.fetch_the_data_fromDB()
        for i in self.yapilacaklar_listesi:
            yeni_gorev = QListWidgetItem()
            yeni_gorev.setText("%5s | %s | %s | %s | %s\n" % (i[0], i[1], i[2], i[3], i[4]))
            self.tasks_list.addItem(yeni_gorev)

    @pyqtSlot()
    def gecmis_taskleri_goruntule_alt(self):
        self.db_bag = databaseConnection.db_connect()
        self.tasks_list.clear()
        self.yapilacaklar_listesi = []
        self.yapilacaklar_listesi = self.db_bag.fetch_the_data_fromDB()
        number_of_the_elements_in_the_list = self.yapilacaklar_listesi.count(self.yapilacaklar_listesi)
        list_strings = []
        for i in self.yapilacaklar_listesi:
            for j in range(number_of_the_elements_in_the_list):
                list_strings.append(self.yapilacaklar_listesi[j])
            self.tasks_list.addItems(list_strings[i])


    @pyqtSlot()
    def task_ekle(self):
        self.pen = penceremiz()
        self.pen.show()

    @pyqtSlot()
    def kapat(self):
        secenek = QMessageBox.question(self, "Programi Sonlandir", "Programi sonlandirmak istedigine emin misin ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if secenek == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    @pyqtSlot()
    def listeye_tiklandi(self):
        print(self.tasks_list.currentItem().text())
        print(self.tasks_list.currentRow())
        # self.db_bag.retrieve_a_row(self.tasks_list.currentRow())

    @pyqtSlot()
    def secilmis_elemani_sil(self):
        # print("Suan tiklanilmis elemanin aslinda ekrandan kaybolmasi gerekiyor")
        # print(self.tasks_list.selectedItems())
        # print(self.tasks_list.currentItem())
        # print("Bu current Item", self.tasks_list.currentItem())
        # print("Bu da row", self.tasks_list.currentRow())
        # print("Secilmis elemani sil methoudundan ", self.db_bag.retrieve_a_row(self.tasks_list.currentRow())[0]) # Bu none geri donduruyor
        self.db_bag.delete_the_clicked_row(self.db_bag.retrieve_a_row(self.tasks_list.currentRow())[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ana_pencere = anaPencere()
    ana_pencere.show()
    sys.exit(app.exec_())