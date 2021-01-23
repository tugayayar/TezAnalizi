import fitz


class HataKontrolleri:

    def __init__(self, tez_nesnesi, tez_yolu):
        self.tez_nesnesi = tez_nesnesi
        self.tez_yolu = tez_yolu
        self.Tezi_Ac()

    def Kontrol_Baslat(self):
        islem_numarasi = []
        message = []
        if (self.Baslik_Kontrolu(self.tez_nesnesi.tez_basligi) == False):
            islem_numarasi.append(1)
            message.append("1-Başlıktaki Her Kelimenin Baş Harfi Büyük Değil")

        if (self.Giris_Yazisi_Kontrolu(self.tez_nesnesi.giris_nesnesi.giris_yazisi) == False):
            islem_numarasi.append(7)
            message.append("7-Giriş Sayfasının İlk Paragrafında Teşekkür İbaresi Yer Alıyor")

        if (self.Sekil_Sayfa_Uyum_Kontrolu(self.tez_nesnesi.sekiller_nesnesi) == False):
            islem_numarasi.append(2)
            message.append("2-Şekiller Listesindeki Şekil Tanımlaması Numarası İle Uyuşmuyor")

        if (self.Cizelge_Sayfa_Uyum_Kontrolu(self.tez_nesnesi.cizelgeler_nesnesi) == False):
            islem_numarasi.append(5)
            message.append("5-Çizelgeler Listesindeki Çizelge Tanımalaması Numarası İle Uyuşmuyor")

        if (self.Denklem_Sayfa_Uyum_Kontrolu(self.tez_nesnesi.denklemler_nesnesi) == False):
            islem_numarasi.append(4)
            message.append("4-Denklemler Listesindeki Denklem Tanımalaması Numarası İle Uyuşmuyor")

        if (self.Tablo_Sayfa_Uyum_Kontrolu(self.tez_nesnesi.tablolar_nesnesi) == False):
            islem_numarasi.append(3)
            message.append("3-Tablolar Listesindeki Tablo Tanımlaması Numarası İle Uyuşmuyor")

        if (self.Referans_Kontrolu(self.tez_nesnesi.referanslar_nesnesi.referanslar_listesi,
                                   self.tez_nesnesi.icerik_nesnesi.sayfalar_listesi) == False):
            islem_numarasi.append(6)
            message.append("6-Referanslarda Tanımalanan Referans Tez İçerisinde Kullanılmamış")

        if (self.Icindekiler_Kontrolu(self.tez_nesnesi.icindekiler_nesnesi) == False):
            islem_numarasi.append(10)
            message.append("10-İçindekiler Kısmındaki Sayfa Numaraları Doğru Değil")

        if (self.Cift_Tirnak_Kontrolu(self.tez_nesnesi.icerik_nesnesi.sayfalar_listesi) == False):
            islem_numarasi.append(8)
            message.append("8-İki Adet Çift Tırnak Arasında 50 Kelimeden Fazla Kelime Kullanılmış")

        if (self.Paragraf_Satir_Kontrolu(self.tez_nesnesi.icerik_nesnesi.sayfalar_listesi) == False):
            islem_numarasi.append(9)
            message.append("9-Paragraf İki Satır ve/veya İki Satırdan Daha Az Satırdan Oluşuyor")
        if len(message) < 1:
            message.append("11-Herhangi bir sorun bulunamadı.")
            islem_numarasi = [11]
        return islem_numarasi, message

    def Baslik_Kontrolu(self, baslik_yazisi):
        baslik_yazisi = baslik_yazisi.split(" ")
        for kelime in baslik_yazisi:
            if len(kelime) > 0 and kelime[0].islower():
                return False
        return True

    def Giris_Yazisi_Kontrolu(self, giris_yazisi):
        ilk_paragraf = ""
        satirlar = giris_yazisi.splitlines()
        i = 0
        while i < len(satirlar) and len(satirlar[i]) >= 5:
            ilk_paragraf = ilk_paragraf + satirlar[i]
            i = i + 1

        if "Teşekkür" in ilk_paragraf or "teşekkür" in ilk_paragraf:
            return False
        return True

    def Sekil_Sayfa_Uyum_Kontrolu(self, sekiller_nesnesi):
        sekiller_listesi = sekiller_nesnesi.sekiller_listesi

        for sekil in sekiller_listesi:
            sayfa_nesnesi = self.pdf_nesnesi.loadPage(sekiller_listesi[sekil])
            sayfa_yazisi = sayfa_nesnesi.getText()
            if sekil not in sayfa_yazisi:
                return False
        return True

    def Cizelge_Sayfa_Uyum_Kontrolu(self, cizelgeler_nesnesi):
        cizelgeler_listesi = cizelgeler_nesnesi.cizelgeler_listesi

        for cizelge in cizelgeler_listesi:
            sayfa_nesnesi = self.pdf_nesnesi.loadPage(cizelgeler_listesi[cizelge])
            sayfa_yazisi = sayfa_nesnesi.getText()
            if cizelge not in sayfa_yazisi:
                return False
        return True

    def Denklem_Sayfa_Uyum_Kontrolu(self, denklemler_nesnesi):
        denklemler_listesi = denklemler_nesnesi.denklemler_listesi

        for denklem in denklemler_listesi:
            sayfa_nesnesi = self.pdf_nesnesi.loadPage(denklemler_listesi[denklem])
            sayfa_yazisi = sayfa_nesnesi.getText()
            if denklem not in sayfa_yazisi:
                return False
        return True

    def Tablo_Sayfa_Uyum_Kontrolu(self, tablolar_nesnesi):
        tablolar_listesi = tablolar_nesnesi.tablolar_listesi

        for tablo in tablolar_listesi:
            sayfa_nesnesi = self.pdf_nesnesi.loadPage(tablolar_listesi[tablo])
            sayfa_yazisi = sayfa_nesnesi.getText()
            if (tablo not in sayfa_yazisi):
                return False
        return True

    def Referans_Kontrolu(self, referanslar_listesi, icerik_sayfa_numaralari):
        for referans in referanslar_listesi:
            is_find = False
            for sayfa_numarasi in icerik_sayfa_numaralari:
                sayfa_nesnesi = self.pdf_nesnesi.loadPage(sayfa_numarasi)
                sayfa_yazisi = sayfa_nesnesi.getText()
                if (referans in sayfa_yazisi):
                    is_find = True
                    break
            if (is_find == False):
                return False
        return True

    def Icindekiler_Kontrolu(self, icindekiler_nesnesi):
        icindekiler_listesi = icindekiler_nesnesi.icindekiler_listesi
        for icindeki in icindekiler_listesi:
            sayfa_nesnesi = self.pdf_nesnesi.loadPage(icindekiler_listesi[icindeki])
            sayfa_yazisi = sayfa_nesnesi.getText()
            if (icindeki not in sayfa_yazisi):
                return False
        return True

    def Cift_Tirnak_Kontrolu(self, icerik_sayfa_numaralari):
        for sayfa_numarasi in icerik_sayfa_numaralari:
            sayfa_nesnesi = self.pdf_nesnesi.loadPage(sayfa_numarasi)
            sayfa_yazisi = sayfa_nesnesi.getText()
            sayfa_yazisi = sayfa_yazisi.split("“")
            if (len(sayfa_yazisi) > 2):
                if (len(sayfa_yazisi[1].split(" ")) >= 50):
                    return False
        return True

    def Paragraf_Satir_Kontrolu(self, icerik_sayfa_numaralari):
        for sayfa_numarasi in icerik_sayfa_numaralari:
            sayfa_nesnesi = self.pdf_nesnesi.loadPage(sayfa_numarasi)
            sayfa_yazisi = sayfa_nesnesi.getText()
            sayfa_satirlari = sayfa_yazisi.splitlines()
            satir_sayaci = 0
            for i in range(len(sayfa_satirlari) - 1):
                if (len(sayfa_satirlari[i]) >= 5):
                    satir_sayaci = satir_sayaci + 1
                else:
                    satir_sayaci = 0

                if len(sayfa_satirlari[i + 1]) < 5 and satir_sayaci <= 2:
                    return False
        return True

    def Tezi_Ac(self):
        self.pdf_nesnesi = fitz.open(self.tez_yolu)
        print(self.pdf_nesnesi)
