import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget
from databaseConnection import DbConnect, DatabaseConnection


class penceremiz(QWidget):
    def __init__(self):
        super(penceremiz, self).__init__()
        self.nameOfTheWindow = 'Bilgi Girme Penceresi'
        self.xPos = 250
        self.yPos = 250
        self.width = 500
        self.height = 350
        self.pencereninKendisiniOlustur()
        self.db_conn = DatabaseConnection()

    def pencereninKendisiniOlustur(self):
        self.setWindowTitle(self.nameOfTheWindow)
        self.setGeometry(self.xPos, self.yPos, self.width, self.height)

        # Edit Text
        self.konuBasligi = QLineEdit()
        self.konuBasligi.setPlaceholderText('Isim Gir')

        self.ismi = QLineEdit()
        self.ismi.setPlaceholderText('Gorevin Adini Gir')

        self.oncelik = QLineEdit()
        self.oncelik.setPlaceholderText('Bunun onceligi nedir')

        self.sontarih = QLineEdit()
        self.sontarih.setPlaceholderText('Son bitis tarihini gir')

        self.yapisSuresi = QLineEdit()
        self.yapisSuresi.setPlaceholderText('Tahmini Yapis Suresini Gir')


        # BUTTONS
        self.kapatmaButtonu = QPushButton('Guncelle')
        self.kapatmaButtonu.clicked.connect(self.bilgileri_al)


        #LAYOUT
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.konuBasligi)
        self.vbox.addWidget(self.ismi)
        self.vbox.addWidget(self.oncelik)
        self.vbox.addWidget(self.sontarih)
        self.vbox.addWidget(self.yapisSuresi)
        self.vbox.addWidget(self.kapatmaButtonu)
        self.setLayout(self.vbox)

    # pyqtSlot un arkasina su parantezleri koymayinca, o zaman farkli bir hata veriyor
    # function degilde string beklendigine dair
    @pyqtSlot()
    def bilgileri_al(self):
        db_bag = DbConnect()
        # db_bag.create_table()
        # db_bag.inserting_new_information(self.konuBasligi.text(), self.ismi.text(), self.oncelik.text(), self.sontarih.text(), self.yapisSuresi.text())
        self.db_conn.insert_doc(self.konuBasligi.text(), self.ismi.text(), self.oncelik.text(), self.sontarih.text(), self.yapisSuresi.text())
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = penceremiz()
    window.show()
    sys.exit(app.exec_())
