from flask import Flask, request, render_template, redirect, url_for,jsonify
import mysql.connector
import serial

app = Flask(__name__)


vtbaglanti = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='ringimnerede')

cursor = vtbaglanti.cursor()

@app.route('/')
def giris():
    return render_template('giris.html')

@app.route('/kayitsayfa')
def kayit():
    return render_template('kayit.html')

@app.route('/anasayfa')
def anasayfa():
    return render_template('anasayfa.html')

@app.route('/saatler')
def saatler():
    return render_template('saatler.html')

@app.route('/duraklar')
def duraklar():
    return render_template('duraklar.html')

@app.route('/giris', methods=['GET', 'POST'])
def giris_post():
    if request.method == 'POST':
        eposta = request.form['eposta']
        sifre = request.form['sifre']

        sorgu = "SELECT sifre,eposta FROM kullanicibilgi WHERE eposta=%s and sifre=%s"
        kbilgi=(eposta,sifre)

        cursor.execute(sorgu,kbilgi)
        sorgusonuc = cursor.fetchall()

        if sorgusonuc:
            return redirect(url_for('anasayfa'))
        else:
            return render_template('giris.html', hata='Yanlış e-posta veya şifre')


@app.route('/kayitekleme', methods=['GET', 'POST'])
def kayitekleme():
    if request.method == 'POST':
        ad = request.form['ad']
        soyad = request.form['soyad']
        eposta = request.form['eposta']
        sifre = request.form['sifre']

        ekle = "INSERT INTO kullanicibilgi (ad, soyad, eposta, sifre) VALUES (%s, %s, %s, %s)"
        cursor.execute(ekle, (ad, soyad, eposta, sifre))
        vtbaglanti.commit()

        return render_template('giris.html')
    else:
        return render_template('kayit.html')

@app.route('/gps-data')
def gps_data():
    try:
        with serial.Serial('COM13', 9600, timeout=1) as ser:  # Windows için COM13 portu
            while True:
                line = ser.readline().decode('ascii', 'ignore').strip()
                if line:
                    #print(f"Received line: {line}")
                    if "Gönderilen veri:" in line:
                        data = line.split(',')
                        if len(data) > 6 and data[2] and data[4]:  # Latitude ve longitude verisi var mı kontrol et
                            latitude = convert_to_degrees(data[2])
                            longitude = convert_to_degrees(data[4])
                            print("a:",latitude)
                            print("b:",longitude)
                            return jsonify({'Enlem': latitude, 'Boylam': longitude})
                        else:
                            print("Geçersiz GPS verisi alındı.")
    except Exception as e:
        print(f"Error: {e}")  # Hata ayıklama için ekleyin
        return jsonify({'error': str(e)})
    return jsonify({'error': 'GPS data not available'})

def convert_to_degrees(raw_value):
    """Convert raw GPS coordinate to degrees"""
    try:
        degrees = int(raw_value[:2])
        minutes = float(raw_value[2:])
        return degrees + (minutes / 60)
    except ValueError:
        return None

if __name__ == '__main__':
    app.run(debug=True)
