import time
import sys
import os

# Tambahkan path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weather_api import get_weather

def test_caching():
    print("=" * 50)
    print("TEST CACHE REDIS")
    print("=" * 50)
    
    # First call - seharusnya lambat (2 detik)
    print("\n[Test 1] First call - memanggil API...")
    start = time.time()
    result1 = get_weather("Jakarta")
    time1 = time.time() - start
    print(f"Waktu: {time1:.2f} detik")
    print(f"Data: {result1}")
    
    # Second call - seharusnya cepat
    print("\n[Test 2] Second call - seharusnya dari cache...")
    start = time.time()
    result2 = get_weather("Jakarta")
    time2 = time.time() - start
    print(f"Waktu: {time2:.2f} detik")
    print(f"Data: {result2}")
    
    # Verifikasi
    print("\n" + "=" * 50)
    if time1 >= 1.5 and time2 < 0.1:
        print("SUKSES: Cache bekerja dengan benar!")
        print(f"Perbedaan waktu: {time1 - time2:.2f} detik lebih cepat")
    else:
        print(f"First call: {time1:.2f}s, Second call: {time2:.2f}s")
        if time1 < 1.5:
            print("Catatan: First call terlalu cepat (harusnya 2 detik)")
        if time2 > 0.1:
            print("Catatan: Second call terlalu lambat (harusnya <0.1 detik)")

if __name__ == "__main__":
    test_caching()