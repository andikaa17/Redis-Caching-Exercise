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