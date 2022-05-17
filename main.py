import numpy as np
from tkinter import * # Windows penceresi için
import matplotlib.pyplot as plt  # Grafik gösterimi için
from sklearn.cluster import KMeans  # K means kümeleme algoritması için
from jqmcvi import base # Dunn index için

#Doğukan Özder
#2018280060

# Txt okur
f = open('C:\\Users\\ZderWindows\\Desktop\\CSC\\S3E1\\VeriMadenciligineGiris\\Final\\Final-data.txt', "r")
satirlar = f.read().split('\n')
f.close()

# Satırlarda "," leri ayırır
veriListesi = []
for i in range(len(satirlar)):
    veriListesi.append(satirlar[i].split(','))

# En baştaki sınıfları ayırır ver veri sayısını bulur
siniflar = satirlar[0].split(',')
sinifSayisi = len(siniflar)
veriListesi.pop(0)
veriSayisi = len(veriListesi) - 1  # -1 olmasının sebebi gönderilen .txt'de son satırın kullanılması

# Veri seti olarak kullanacağımız arrayi tanımlar
veriSetiInt = np.ndarray(shape=(veriSayisi, sinifSayisi), dtype=int)
veriSetiMin = []
veriSetiMax = []
for i in range(sinifSayisi):
    veriSetiMin.append(int(veriListesi[0][i]))
    veriSetiMax.append(int(veriListesi[0][i]))

# Veri seti normalizasyonu için minimum ve maximum değerleri bulur
for i in range(veriSayisi):
    for j in range(sinifSayisi):
        if veriSetiMin[j] > int(veriListesi[i][j]):
            veriSetiMin[j] = int(veriListesi[i][j])
        if veriSetiMax[j] < int(veriListesi[i][j]):
            veriSetiMax[j] = int(veriListesi[i][j])
        veriSetiInt[i][j] = int(veriListesi[i][j])

# Normalize edilmiş veri seti için arrayi oluşturur ve verileri normalize eder
veriSetiNorm = np.ndarray(shape=(veriSayisi, sinifSayisi), dtype=float)
for i in range(veriSayisi):
    for j in range(sinifSayisi):
        veriSetiNorm[i][j] = float((veriSetiInt[i][j] - veriSetiMin[j]) / (veriSetiMax[j] - veriSetiMin[j]))


# Veri görselleştirme butonunun fonksiyonu
def veri_gorsellestirme():
    if grafik1deger.get() == "Lütfen Grafik 1'i Seçiniz" or grafik2deger.get() == "Lütfen Grafik 2'yi Seçiniz" or not kumeSayisi.get().isnumeric():
        print("Değer Eksik!")
    else:
        plt.close()
        # Kmeans algoritmasını çalıştırır ve kümeleri kaydeder
        kmeans = KMeans(n_clusters=int(kumeSayisi.get()))
        kmeans.fit(veriSetiNorm)
        kumeler = kmeans.cluster_centers_

        # Verilerin küme indexlerini kaydeder
        y_km = kmeans.fit_predict(veriSetiNorm)

        renkler = ["red", "blue", "green", "purple", "violet", "cyan", "magenta", "orange"]

        # Verileri grafikte farklı renkler ile gösterir
        for i in range(len(kumeler)):
            plt.scatter(veriSetiNorm[y_km == i, siniflar.index(grafik1deger.get())],
                        veriSetiNorm[y_km == i, siniflar.index(grafik2deger.get())],
                        s=35, color=renkler[i % len(renkler)])

        # Küme merkezlerini grafikte yıldız şeklinde gösterir
        for i in range(len(kumeler)):
            plt.scatter(kumeler[i][siniflar.index(grafik1deger.get())],
                        kumeler[i][siniflar.index(grafik2deger.get())],
                        marker='*',
                        s=150,
                        color="black")

        plt.show()


# Verileri kaydet butonunun fonksiyonu
def txt_kaydet():
    if not kumeSayisi.get().isnumeric():
        print("Değer Eksik!")
    else:
        # Kmeans algoritmasını çalıştırır ve kümeleri kaydeder
        kmeans = KMeans(n_clusters=int(kumeSayisi.get()))
        kmeans.fit(veriSetiNorm)
        kumeler = kmeans.cluster_centers_

        # Verilerin küme indexlerini kaydeder
        y_km = kmeans.fit_predict(veriSetiNorm).tolist()

        # BCSS için değerleri hesaplar
        _, labelSayisi = np.unique(kmeans.labels_, return_counts=True)
        kumelerArasiFarkinKaresi = np.linalg.norm(kumeler - np.mean(veriSetiNorm, axis=0), axis=1) ** 2

        WCSS = kmeans.inertia_
        BCSS = sum(labelSayisi * kumelerArasiFarkinKaresi)
        DUNN = base.dunn(kumeler)*1000

        WCSS = "{:.2f}".format(WCSS)
        BCSS = "{:.2f}".format(BCSS)
        DUNN = "{:.2f}".format(DUNN)

        dosya = open("sonuc.txt", "w")
        # Kayıtları ve hangi kümede olduklarını yazdırır
        for i in range(len(veriSetiInt)):
            dosya.write(f"Kayıt {i+1}:\tKüme {y_km[i]+1}\n")

        # Her kümede kaç kayıt olduğunu yazdırır
        for i in range(len(kumeler)):
            dosya.write(f"\nKüme {i+1}:\t{y_km.count(i)} kayıt")

        # WCSS BCSS ve Dunn Index değerlerini yazdırır
        dosya.write(f"\n\nWCSS: {WCSS}\nBCSS: {BCSS}\nDunn Index: {DUNN}")
        print("sonuc.txt adlı dosyaya yazılmıştır.")
        dosya.close()


# Windows penceresi oluşturur
window = Tk()
window.title('Doğukan Özder')
window.geometry("500x500")

# Grafiğin 1. değeri için option menu oluşturur
grafik1deger = StringVar(window)
grafik1deger.set("Lütfen Grafik 1'i Seçiniz")
grafik1 = OptionMenu(window, grafik1deger, *siniflar)
grafik1.pack(fill=BOTH)

# Grafiğin 2. değeri için option menu oluşturur
grafik2deger = StringVar(window)
grafik2deger.set("Lütfen Grafik 2'yi Seçiniz")
grafik2 = OptionMenu(window, grafik2deger, *siniflar)
grafik2.pack(fill=BOTH, side=TOP)

# Entry üstüne K değerini giriniz yazar
L1 = Label(window, text="K Değerini Giriniz")
L1.pack(fill=BOTH)

# Küme sayısı için k değer ister
kumeSayisi = Entry(window)
kumeSayisi.pack()

# Veri görselleştirme butonunu oluşturur
gorsellestir = Button(window, text="Veri Görselleştirme", command=veri_gorsellestirme)
gorsellestir.pack(fill=BOTH, side=TOP)

# Verileri kaydet butonunu oluşturur
kaydet = Button(window, text="Verileri Kaydet", command=txt_kaydet)
kaydet.pack(fill=BOTH, side=TOP)

window.mainloop()
