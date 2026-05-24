# Laporan Praktikum: Caching API dengan Redis

## Mata Kuliah

Pemrograman Side Server (PSS)

## Judul Tugas

Implementasi Caching Sederhana Menggunakan Redis untuk Menyimpan Hasil API Call

---

## Bagian 1: Kode Program

### Kode Awal (Sebelum Ada Cache)

weather_api.py - KODE INI SUDAH DIBERIKAN
import requests
import time

def get_weather(city):
"""Simulasi API call yang lambat"""
time.sleep(2) # Simulate slow API
response = requests.get(f"https://api.example.com/weather/{city}")
return response.json()
Problem: Setiap panggil get_weather() butuh 2 detik
Solution: Cache hasilnya di Redis selama 5 menit

### Kode Akhir (Sudah Pakai Redis Cache)

import time
import json
import redis

# Koneksi ke Redis

r = redis.Redis(
host='redis',
port=6379,
db=0,
decode_responses=True
)

def get_weather(city):
cache_key = f"weather:{city.lower()}"

    # GET - cek cache dulu
    cached_data = r.get(cache_key)
    if cached_data:
        print("Data diambil dari CACHE Redis")
        return json.loads(cached_data)

    # Jika tidak ada di cache, panggil API
    print("Data diambil dari API (lambat)...")
    time.sleep(2)

    weather_data = {
        "city": city,
        "temperature": 30,
        "condition": "Cerah",
        "humidity": 65
    }

    # SET - simpan data ke Redis
    r.set(cache_key, json.dumps(weather_data))

    # EXPIRE - set masa berlaku 5 menit (300 detik)
    r.expire(cache_key, 300)

    return weather_data

## Bagian 2: Perintah Redis yang Digunakan

- GET Digunakan untuk mengambil data dari cache. Di kode saya, r.get(cache_key) berfungsi mengecek apakah data cuaca sudah tersimpan di Redis.

- SET Digunakan untuk menyimpan data ke cache. Di kode saya, r.set(cache_key, json.dumps(weather_data)) menyimpan data cuaca ke Redis setelah berhasil dipanggil dari API.

- EXPIRE Digunakan untuk mengatur masa berlaku data. Di kode saya, r.expire(cache_key, 300) membuat data otomatis dihapus setelah 5 menit (300 detik).

## Bagian 3 : Hasil Pengujian

3.1 Status Container Docker
Perintah yang dijalankan: Docker Compose ps
![alt text](image.png)

3.2 Test Ping
Perintah yang dijalankan: docker compose exec redis redis-cli ping
![alt text](image-1.png)

3.3 Hasil Test Cache
Perintah yang dijalankan: docker compose exec app python test_cache.py
![alt text](image-2.png)

3.4 Verifikasi Data di Redis
Perintah yang dijalankan:
docker compose exec redis redis-cli
KEYS \*
GET weather:jakarta
TTL weather:jakarta
exit
![alt text](image-3.png)

## Bagian 4 : Jawaban Pertanyaan

4.1 Kenapa response time berbeda?
Karena first call data belum ada di cache sehingga harus memanggil API dulu yang membutuhkan waktu 2 detik, sedangkan second call data sudah tersimpan di Redis sehingga langsung diambil dari cache dan hanya butuh waktu 0 detik.

4.2 Apa keuntungan caching?
Keuntungan caching adalah response time menjadi lebih cepat, beban server API berkurang, biaya request ke API eksternal lebih hemat, dan aplikasi menjadi lebih responsif.

4.3 Kapan sebaiknya tidak menggunakan cache?
Cache sebaiknya tidak digunakan ketika data harus real-time seperti harga saham atau skor bola, ketika data berubah sangat sering, ketika data bersifat sensitif seperti password atau rekening bank, dan ketika memori server terbatas.

---

Penjelasan - Third call after 5 minutes
Setelah 5 menit cache akan expired atau hapus sendiri, sehingga sistem harus memanggil API lagi dan waktu respons akan kembali lambat sekitar 2 detik.

Kesimpulan
Implementasi caching dengan Redis berhasil mempercepat response time dari 2.02 detik menjadi 0.00 detik. Redis mudah diimplementasikan dengan perintah GET, SET, dan EXPIRE. Cache sangat berguna untuk data yang tidak sering berubah, namun tidak cocok untuk data real-time atau data sensitif.
