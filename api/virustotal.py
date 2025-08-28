import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv() # Memuat variabel dari file .env

# Ambil API Key dari environment variable
API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

def check_virustotal(url):
    """
    Mengecek URL menggunakan VirusTotal API v3 dan mengembalikan data atribut.
    """
    if not API_KEY:
        return {"error": "VIRUSTOTAL_API_KEY tidak ditemukan di file .env"}
        
    try:
        # Encode URL ke format base64 yang aman untuk URL
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        headers = {
            "x-apikey": API_KEY,
            "accept": "application/json"
        }
        
        # Lakukan request ke VirusTotal API
        response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
        
        response.raise_for_status()
        
        attributes = response.json().get('data', {}).get('attributes', {})
        return attributes

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        if err.response.status_code == 404:
            return {"error": "URL tidak ditemukan di database VirusTotal."}
        return {"error": f"Gagal mendapatkan data: {err}"}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": "Terjadi kesalahan saat memproses permintaan."}
