import requests
import socket
import os
from dotenv import load_dotenv

load_dotenv() # Memuat variabel dari file .env

# Ambil Access Token dari environment variable
ACCESS_TOKEN = os.getenv("IPINFO_TOKEN")

def get_ip_geolocation(domain):
    """
    Mendapatkan alamat IP dari domain dan mencari data geolokasinya.
    """
    if not ACCESS_TOKEN:
        return {"error": "IPINFO_TOKEN tidak ditemukan di file .env"}
        
    try:
        ip_address = socket.gethostbyname(domain)
    except socket.gaierror:
        return {"error": "Tidak dapat menemukan alamat IP untuk domain ini."}
    except Exception as e:
        return {"error": f"Terjadi kesalahan saat mencari IP: {e}"}

    try:
        api_url = f"https://ipinfo.io/{ip_address}"
        params = {"token": ACCESS_TOKEN}
        
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data

    except requests.exceptions.HTTPError as err:
        return {"error": f"Gagal menghubungi server geolokasi. ({err})"}
    except Exception as e:
        return {"error": f"Terjadi kesalahan saat mengambil data geolokasi: {e}"}
