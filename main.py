import sys
import requests
import sqlite3 as sqlite
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPixmap


class HavaDurumuUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hava Durumu')
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.background_image = QLabel(self)
        self.background_pixmap = QPixmap("C:/Users/fatih/OneDrive/Masaüstü/Hava Durumu/bulutlu.jpg")
        self.background_image.setPixmap(self.background_pixmap)

        layout.addWidget(self.background_image)

        self.sehir_girdi = QLineEdit()
        layout.addWidget(self.sehir_girdi)

        self.hava_durumu_al_button = QPushButton('Hava Durumu Al ve Kaydet')
        self.hava_durumu_al_button.clicked.connect(self.hava_durumu_al_ve_kaydet)
        layout.addWidget(self.hava_durumu_al_button)

        self.hava_durumu_etiket = QLabel()
        layout.addWidget(self.hava_durumu_etiket)

        self.central_widget.setLayout(layout)

        self.conn = sqlite.connect('hava_durumu.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS hava_durumu
                             (sehir TEXT, sicaklik REAL, nem REAL, aciklama TEXT)''')
        self.conn.commit()


    def set_background_image(self, hava):
        if hava == 'Parçalı bulutlu':
            image_path = "C:/Users/fatih/OneDrive/Masaüstü/Hava Durumu/parçalı_bulutlu.jpg"
        elif hava == 'Hava açık':
            image_path = "C:/Users/fatih\OneDrive\Masaüstü\Hava Durumu/açık_hava.jpg"
        elif hava == 'Bulutlu':
            image_path = "C:/Users/fatih/OneDrive/Masaüstü/Hava Durumu/bulutlu.jpg"
        else:
            image_path = "C:/Users/fatih/OneDrive/Masaüstü/Hava Durumu/az_bulutlu.jpg"

        self.background_pixmap = QPixmap(image_path)
        self.background_image.setPixmap(self.background_pixmap)


    def hava_durumu_al_ve_kaydet(self):
        sehir = self.sehir_girdi.text()

        API_ID = '49898c37c4e665a267f1be966e979f87'
        URL = 'http://api.openweathermap.org/data/2.5/weather'

        params = {
            'q': sehir,
            'appid': API_ID,
            'units': 'metric'
        }

        yanit = requests.get(URL, params=params)
        veri = yanit.json()

        sicaklik = veri['main']['temp']
        nem = veri['main']['humidity']
        aciklama = veri['weather'][0]['description']

        if aciklama == 'scattered clouds':
            aciklama = 'Parçalı bulutlu'
        elif aciklama == 'clear sky':
            aciklama = 'Hava açık'
        elif aciklama == 'broken clouds':
            aciklama = 'Parçalı bulutlu'
        elif aciklama == 'overcast clouds':
            aciklama = 'Bulutlu'
        elif aciklama == 'few clouds':
            aciklama = 'Az bulutlu'

        self.set_background_image(aciklama)

        threading.Thread(target=self.hava_durumu_al_ve_kaydet_thread, args=(sehir,)).start()

    def hava_durumu_al_ve_kaydet_thread(self, sehir):
        API_ID = '49898c37c4e665a267f1be966e979f87'
        URL = 'http://api.openweathermap.org/data/2.5/weather'

        params = {
            'q': sehir,
            'appid': API_ID,
            'units': 'metric'
        }

        yanit = requests.get(URL, params=params)
        veri = yanit.json()

        sicaklik = veri['main']['temp']
        nem = veri['main']['humidity']
        aciklama = veri['weather'][0]['description']

        if aciklama == 'scattered clouds':
            aciklama = 'Parçalı bulutlu'
        elif aciklama == 'clear sky':
            aciklama = 'Hava açık'
        elif aciklama == 'broken clouds':
            aciklama = 'Parçalı bulutlu'
        elif aciklama == 'overcast clouds':
            aciklama = 'Bulutlu'
        elif aciklama == 'few clouds':
            aciklama = 'Az bulutlu'

        hava_durumu_bilgi = f"{sehir} şehri için hava durumu bilgileri:\n"
        hava_durumu_bilgi += f"Sıcaklık: {sicaklik}°C\n"
        hava_durumu_bilgi += f"Nem: {nem}%\n"
        hava_durumu_bilgi += f"Hava Durumu: {aciklama}"

        self.hava_durumu_etiket.setText(hava_durumu_bilgi)

        self.cursor.execute('INSERT INTO hava_durumu VALUES (?, ?, ?, ?)', (sehir, sicaklik, nem, aciklama))
        self.conn.commit()

    def closeEvent(self, event):
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = HavaDurumuUygulamasi()
    pencere.show()
    sys.exit(app.exec_())


