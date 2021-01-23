from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from ui_arayuz import Ui_MainWindow
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.self_setup_ui()
        self.initSlots()
        self.initParameters()
        self.test()

        self.ui.btn_pdf_analiz_yap.setEnabled(True)
        self.ui.listWidget.setStyleSheet("color: rgb(255, 255, 255);")
        self.show()

    def control(self):
        if len(self.ui.txt_dosya_yolu.text()) < 5:
            self.ui.btn_pdf_analiz_yap.setEnabled(False)
        else:
            self.ui.btn_pdf_analiz_yap.setEnabled(True)

    def initParameters(self):
        self.icindekiler_listesi_sayfa_numaralari = []
        self.sekiller_listesi_sayfa_numaralari = []
        self.tablolar_listesi_sayfa_numaralari = []
        self.denklemler_listesi_sayfa_numaralari = []
        self.referanslar_listesi_sayfa_numaralari = []
        self.cizelgeler_listesi_sayfa_numaralari = []
        self.giris_sayfa_numaralari = []
        self.tez_baslangic_sayfasi = None
        self.baslik_sayfasi = []

    def initSlots(self):
        self.ui.btn_dosya_sec.clicked.connect(self.dosya_sec)
        self.ui.action_dosya_sec.triggered.connect(self.dosya_sec)
        self.ui.btn_pdf_analiz_yap.clicked.connect(self.getParameters)
        self.ui.action_gelistiriciler.triggered.connect(self.kilavuz)

    def kilavuz(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle("Projedeki Kişiler")
        self.msg.setText("Geliştiriciler                                                      ")
        self.msg.setInformativeText("TUGAY AYAR\nAKIN BURAK YAZLIK\nMUHAMMET YASİN YILDIZ\nİSMAİL ÇAĞAN")
        self.msg.show()

    def self_setup_ui(self):
        self.ui.txt_dosya_yolu.setEnabled(False)
        """self.ui.txt_no_giris.setValidator(QDoubleValidator())
        self.ui.txt_no_sekiller.setValidator(QDoubleValidator())
        self.ui.txt_no_baslik.setValidator(QDoubleValidator())
        self.ui.txt_no_cizelge.setValidator(QDoubleValidator())
        self.ui.txt_no_tablolar.setValidator(QDoubleValidator())
        self.ui.txt_no_baslangic.setValidator(QDoubleValidator())
        self.ui.txt_no_denklemler.setValidator(QDoubleValidator())
        self.ui.txt_no_icindekiler.setValidator(QDoubleValidator())
        self.ui.txt_no_referans.setValidator(QDoubleValidator())"""

    def test(self):
        self.ui.txt_no_giris.setText("12,13,14")
        self.ui.txt_no_baslik.setText("1")
        self.ui.txt_no_cizelge.setText("9,10")
        self.ui.txt_no_sekiller.setText("11")
        self.ui.txt_no_tablolar.setText("")
        self.ui.txt_no_baslangic.setText("12")
        self.ui.txt_no_denklemler.setText("")
        self.ui.txt_no_icindekiler.setText("7,8")
        self.ui.txt_no_referans.setText("105, 106, 107, 108, 109, 110, 111, 112")

    def dosya_sec(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.pdf)")
        self.tez_yolu = fname[0]
        self.ui.txt_dosya_yolu.setText(self.tez_yolu)
        self.control()

    def getParameters(self):

        if len(self.ui.txt_no_giris.text()) > 0:
            for i in self.ui.txt_no_giris.text().split(","):
                self.giris_sayfa_numaralari.append(int(i))

        if len(self.ui.txt_no_referans.text()) > 0:
            for i in self.ui.txt_no_referans.text().split(","):
                self.referanslar_listesi_sayfa_numaralari.append(int(i))

        if len(self.ui.txt_no_baslik.text()) > 0:
            self.baslik_sayfasi = int(self.ui.txt_no_baslik.text())

        if len(self.ui.txt_no_cizelge.text()) > 0:
            for i in self.ui.txt_no_cizelge.text().split(","):
                self.cizelgeler_listesi_sayfa_numaralari.append(int(i))

        if len(self.ui.txt_no_icindekiler.text()) > 0:
            for i in self.ui.txt_no_icindekiler.text().split(","):
                self.icindekiler_listesi_sayfa_numaralari.append(int(i))

        if len(self.ui.txt_no_denklemler.text()) > 0:
            for i in self.ui.txt_no_denklemler.text().split(","):
                self.denklemler_listesi_sayfa_numaralari.append(int(i))

        if len(self.ui.txt_no_baslangic.text()) > 0:
            self.tez_baslangic_sayfasi = int(self.ui.txt_no_baslangic.text())

        if len(self.ui.txt_no_tablolar.text()) > 0:
            for i in self.ui.txt_no_tablolar.text().split(","):
                self.tablolar_listesi_sayfa_numaralari.append(int(i))

        if len(self.ui.txt_no_sekiller.text()) > 0:
            for i in self.ui.txt_no_sekiller.text().split(","):
                self.sekiller_listesi_sayfa_numaralari.append(int(i))

        self.analiz_baslat()

    def analiz_baslat(self):
        from HataKontrol import HataKontrolleri
        from TezAnalizi import PdfIslemleri
        pdf_islemleri = PdfIslemleri(
            self.baslik_sayfasi,
            self.tez_yolu,
            self.icindekiler_listesi_sayfa_numaralari,
            self.sekiller_listesi_sayfa_numaralari,
            self.tablolar_listesi_sayfa_numaralari,
            self.denklemler_listesi_sayfa_numaralari,
            self.cizelgeler_listesi_sayfa_numaralari,
            self.referanslar_listesi_sayfa_numaralari,
            self.giris_sayfa_numaralari,
            self.tez_baslangic_sayfasi
        )
        tez = pdf_islemleri.Tez_Nesnesi_Olustur()
        hata_kontrol_nesnesi = HataKontrolleri(tez, self.tez_yolu)
        self.result, self.message = hata_kontrol_nesnesi.Kontrol_Baslat()
        print(self.result)
        print(type(self.result))
        self.message2 = pdf_islemleri.messageBox
        self.addItemToListWidget()

    def addItemToListWidget(self):
        self.ui.listWidget.addItems(self.message2)
        self.ui.listWidget.addItem("")
        self.ui.listWidget.addItems(self.message)
        # self.ui.listWidget.addItems(self.result)
        print(self.result)
        self.ui.tabWidget.setCurrentIndex(1)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    loginWindow = MainWindow()
    loginWindow.show()
    sys.exit(app.exec_())
