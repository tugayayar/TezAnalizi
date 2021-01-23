# içindekiler
# şekiller
# tablolar
# denklemler
# referanslar
# giriş
# içerik


import fitz
from Fonksiyonlar import Icindekiler, Sekiller, Tablolar, Denklemler, Referanslar, Giris, Cizelgeler, Icerik, Tez
from HataKontrol import HataKontrolleri


class PdfIslemleri:
    # Değişken tanımlamaları
    tez_yolu = ""
    tez_okuyucu = ""
    tez_nesnesi = ""
    icindekiler_listesi_sayfa_numaralari = []
    sekiller_listesi_sayfa_numaralari = []
    tablolar_listesi_sayfa_numaralari = []
    denklemler_listesi_sayfa_numaralari = []
    referanslar_listesi_sayfa_numaralari = []
    giris_sayfa_numaralari = []
    cizelgeler_sayfa_numaralari = []
    tez_baslangic_sayfasi = 0
    baslik_sayfa_numarasi = 0
    baslik = ""

    # Nesne tanımlamaları
    icindekiler_nesnesi = Icindekiler()
    sekiller_nesnesi = Sekiller()
    tablolar_nesnesi = Tablolar()
    denklemler_nesnesi = Denklemler()
    referanslar_nesnesi = Referanslar()
    giris_nesnesi = Giris()
    cizelgeler_nesnesi = Cizelgeler()
    icerik_nesnesi = Icerik()

    def __init__(self, tez_baslik_sayfa_numarasi, pdf_tez_yolu, icindekiler_sayfalari, sekiller_sayfalari,
                 tablolar_sayfalari, denklemler_sayfalari, cizelgeler_sayfalari, referanslar_sayfalari, giris_sayfalari,
                 tez_baslangic_sayfasi):
        self.tez_yolu = pdf_tez_yolu
        self.icindekiler_listesi_sayfa_numaralari = icindekiler_sayfalari
        self.sekiller_listesi_sayfa_numaralari = sekiller_sayfalari
        self.tablolar_listesi_sayfa_numaralari = tablolar_sayfalari
        self.denklemler_listesi_sayfa_numaralari = denklemler_sayfalari
        self.referanslar_listesi_sayfa_numaralari = referanslar_sayfalari
        self.giris_sayfa_numaralari = giris_sayfalari
        self.cizelgeler_listesi_sayfa_numaralari = cizelgeler_sayfalari
        self.tez_baslangic_sayfasi = tez_baslangic_sayfasi - 1
        self.baslik_sayfa_numarasi = tez_baslik_sayfa_numarasi - 1
        self.messageBox = []
        self.Tezi_Ac()

    def Tezi_Ac(self):
        self.tez_nesnesi = fitz.open(self.tez_yolu)
        self.Tezi_Parcala()

    def Tez_Nesnesi_Olustur(self):
        return Tez(self.baslik,
                   self.icindekiler_nesnesi,
                   self.sekiller_nesnesi,
                   self.tablolar_nesnesi,
                   self.denklemler_nesnesi,
                   self.cizelgeler_nesnesi,
                   self.referanslar_nesnesi,
                   self.giris_nesnesi,
                   self.icerik_nesnesi)

    def Tezi_Parcala(self):
        en_buyuk_giris_sayfasi = 0
        if (len(self.icindekiler_listesi_sayfa_numaralari) > 0):
            for sayfa_numarasi in self.icindekiler_listesi_sayfa_numaralari:
                sayfa_nesnesi = self.tez_nesnesi.loadPage(sayfa_numarasi - 1)
                sayfa_yazisi = sayfa_nesnesi.getText()
                sayfa_satirlari = sayfa_yazisi.splitlines()
                baslik = ""
                numara = ""
                for satir in sayfa_satirlari:
                    guncel_satir = satir.strip()

                    if (baslik != "" and len(guncel_satir) > 0 and guncel_satir.isdigit()):
                        numara = guncel_satir
                        self.icindekiler_nesnesi.eleman_ekle(baslik + " " + numara, self.tez_baslangic_sayfasi)
                        numara = ""
                        baslik = ""

                    elif (baslik != "" and len(guncel_satir) > 0):
                        baslik = baslik + " " + guncel_satir

                    if (len(guncel_satir) > 4):
                        if (guncel_satir[0].isdigit() and (guncel_satir[1] == '.' or guncel_satir[2] == '.')):
                            baslik = guncel_satir
                if (en_buyuk_giris_sayfasi < sayfa_numarasi):
                    en_buyuk_giris_sayfasi = sayfa_numarasi
            print(self.icindekiler_nesnesi.icindekiler_listesi)
            print("İçerik Kısmı Derlendi...")
            self.messageBox.append("İçerik Kısmı Derlendi...")

        if (len(self.sekiller_listesi_sayfa_numaralari) > 0):
            for sayfa_numarasi in self.sekiller_listesi_sayfa_numaralari:
                sayfa_nesnesi = self.tez_nesnesi.loadPage(sayfa_numarasi - 1)
                sayfa_yazisi = sayfa_nesnesi.getText()
                sayfa_satirlari = sayfa_yazisi.splitlines()
                baslik = ""
                numara = ""
                for satir in sayfa_satirlari:
                    guncel_satir = satir.strip()

                    if (baslik != "" and len(guncel_satir) > 0 and guncel_satir.isdigit()):
                        numara = guncel_satir
                        self.sekiller_nesnesi.eleman_ekle(baslik + " " + numara, self.tez_baslangic_sayfasi)
                        numara = ""
                        baslik = ""

                    elif (baslik != "" and len(guncel_satir) > 0):
                        baslik = baslik + " " + guncel_satir

                    if (len(guncel_satir) > 4):
                        if (guncel_satir.split(" ")[0] == "Şekil"):
                            baslik = guncel_satir
                if (en_buyuk_giris_sayfasi < sayfa_numarasi):
                    en_buyuk_giris_sayfasi = sayfa_numarasi
            print(self.sekiller_nesnesi.sekiller_listesi)
            print("Şekiller Listesi Derlendi...")
            self.messageBox.append("Şekiller Listesi Derlendi...")

        if (len(self.tablolar_listesi_sayfa_numaralari) > 0):
            for sayfa_numarasi in self.tablolar_listesi_sayfa_numaralari:
                sayfa_nesnesi = self.tez_nesnesi.loadPage(sayfa_numarasi - 1)
                sayfa_yazisi = sayfa_nesnesi.getText()
                sayfa_satirlari = sayfa_yazisi.splitlines()
                baslik = ""
                numara = ""
                for satir in sayfa_satirlari:
                    guncel_satir = satir.strip()

                    if (baslik != "" and len(guncel_satir) > 0 and guncel_satir.isdigit()):
                        numara = guncel_satir
                        self.tablolar_nesnesi.eleman_ekle(baslik + " " + numara, self.tez_baslangic_sayfasi)
                        numara = ""
                        baslik = ""

                    elif (baslik != "" and len(guncel_satir) > 0):
                        baslik = baslik + " " + guncel_satir

                    if (len(guncel_satir) > 4):
                        if (guncel_satir.split(" ")[0] == "Tablo"):
                            baslik = guncel_satir
                if (en_buyuk_giris_sayfasi < sayfa_numarasi):
                    en_buyuk_giris_sayfasi = sayfa_numarasi
            # print(self.tablolar_nesnesi.tablolar_listesi)
            print("Tablolar Listesi Derlendi...")
            self.messageBox.append("Tablolar Listesi Derlendi...")

        if (len(self.denklemler_listesi_sayfa_numaralari) > 0):
            for sayfa_numarasi in self.denklemler_listesi_sayfa_numaralari:
                sayfa_nesnesi = self.tez_nesnesi.loadPage(sayfa_numarasi - 1)
                sayfa_yazisi = sayfa_nesnesi.getText()
                sayfa_satirlari = sayfa_yazisi.splitlines()
                baslik = ""
                numara = ""
                for satir in sayfa_satirlari:
                    guncel_satir = satir.strip()

                    if (baslik != "" and len(guncel_satir) > 0 and guncel_satir.isdigit()):
                        numara = guncel_satir
                        self.denklemler_nesnesi.eleman_ekle(baslik + " " + numara, self.tez_baslangic_sayfasi)
                        numara = ""
                        baslik = ""

                    elif (baslik != "" and len(guncel_satir) > 0):
                        baslik = baslik + " " + guncel_satir

                    if (len(guncel_satir) > 4):
                        if (guncel_satir.split(" ")[0] == "Denklem"):
                            baslik = guncel_satir
                if (en_buyuk_giris_sayfasi < sayfa_numarasi):
                    en_buyuk_giris_sayfasi = sayfa_numarasi
            # print(self.denklemler_nesnesi.denklemler_listesi)
            print("Denklemler Listesi Derlendi...")
            self.messageBox.append("Denklemler Listesi Derlendi...")

        if (len(self.cizelgeler_listesi_sayfa_numaralari) > 0):
            for sayfa_numarasi in self.cizelgeler_listesi_sayfa_numaralari:
                sayfa_nesnesi = self.tez_nesnesi.loadPage(sayfa_numarasi - 1)
                sayfa_yazisi = sayfa_nesnesi.getText()
                sayfa_satirlari = sayfa_yazisi.splitlines()
                baslik = ""
                numara = ""
                for satir in sayfa_satirlari:
                    guncel_satir = satir.strip()

                    if (baslik != "" and len(guncel_satir) > 0 and guncel_satir.isdigit()):
                        numara = guncel_satir
                        self.cizelgeler_nesnesi.eleman_ekle(baslik + " " + numara, self.tez_baslangic_sayfasi)
                        numara = ""
                        baslik = ""

                    elif (baslik != "" and len(guncel_satir) > 0):
                        baslik = baslik + " " + guncel_satir

                    if (len(guncel_satir) > 4):
                        if (guncel_satir.split(" ")[0] == "Çizelge"):
                            baslik = guncel_satir
                if (en_buyuk_giris_sayfasi < sayfa_numarasi):
                    en_buyuk_giris_sayfasi = sayfa_numarasi
            # print(self.cizelgeler_nesnesi.cizelgeler_listesi)
            print("Çizelgeler Listesi Derlendi...")
            self.messageBox.append("Çizelgeler Listesi Derlendi...")

        if (len(self.referanslar_listesi_sayfa_numaralari) > 0):
            for sayfa_numarasi in self.referanslar_listesi_sayfa_numaralari:
                sayfa_nesnesi = self.tez_nesnesi.loadPage(sayfa_numarasi - 1)
                sayfa_yazisi = sayfa_nesnesi.getText()
                sayfa_satirlari = sayfa_yazisi.splitlines()
                baslik = ""
                numara = ""
                onceki_satir = ""
                for satir in sayfa_satirlari:
                    guncel_satir = satir.strip()
                    if (len(guncel_satir) > 4 and len(onceki_satir) <= 4):
                        baslik = guncel_satir
                        self.referanslar_nesnesi.eleman_ekle(baslik)
                    onceki_satir = satir
            # print(self.referanslar_nesnesi.referanslar_listesi)
            print("Referanslar Listesi Derlendi...")
            self.messageBox.append("Referanslar Listesi Derlendi...")

        if (len(self.giris_sayfa_numaralari) > 0):
            for sayfa_numarasi in self.giris_sayfa_numaralari:
                sayfa_nesnesi = self.tez_nesnesi.loadPage(sayfa_numarasi - 1)
                sayfa_yazisi = sayfa_nesnesi.getText()
                self.giris_nesnesi.eleman_ekle(sayfa_yazisi)
            # print(str(len(self.giris_nesnesi.giris_yazisi)) + " adet harf içeriyor")
            print("Giriş Yazısı Derlendi...")
            self.messageBox.append("Giriş Yazısı Derlendi...")

        self.icerik_nesnesi.icerigi_guncelle(en_buyuk_giris_sayfasi + 1,
                                             self.referanslar_listesi_sayfa_numaralari[0] - 1)
        # print(self.icerik_nesnesi.sayfalar_listesi)
        print("İçerik Kısmının Sayfa Numaraları Güncellendi...")
        self.messageBox.append("İçerik Kısmının Sayfa Numaraları Güncellendi...")

        sayfa_nesnesi = self.tez_nesnesi.loadPage(self.baslik_sayfa_numarasi)
        sayfa_yazisi = sayfa_nesnesi.getText()
        sayfa_satirlari = sayfa_yazisi.splitlines()
        bos_satir_sayisi = 0
        baslik_satiri_baslangici = 0
        for i in range(len(sayfa_satirlari)):
            if (len(sayfa_satirlari[i]) < 2):
                bos_satir_sayisi = bos_satir_sayisi + 1
            if (len(sayfa_satirlari[i]) >= 5 and bos_satir_sayisi >= 3):
                baslik_satiri_baslangici = i
                break

        while (baslik_satiri_baslangici < len(sayfa_satirlari) and len(sayfa_satirlari[baslik_satiri_baslangici]) >= 5):
            self.baslik = self.baslik + sayfa_satirlari[baslik_satiri_baslangici] + " "
            baslik_satiri_baslangici = baslik_satiri_baslangici + 1
        # print(self.baslik)
        print("Başlık Kısmı Başarı İle Derlendi...")
        self.messageBox.append("Başlık Kısmı Başarı İle Derlendi...")
