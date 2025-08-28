import requests
import os
from dotenv import load_dotenv

load_dotenv() # Memuat variabel dari file .env

# Ambil API Key dari environment variable
API_KEY = os.getenv("WHOIS_API_KEY")

def get_whois_data(domain):
    """
    Mengambil data WHOIS untuk domain menggunakan WhoisXML API.
    """
    if not API_KEY:
        return {"error": "WHOIS_API_KEY tidak ditemukan di file .env"}

    api_url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"

    params = {
        "apiKey": API_KEY,
        "domainName": domain,
        "outputFormat": "JSON"
    }

    try:
        response = requests.get(api_url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        
        if "ErrorMessage" in data:
            return {"error": data["ErrorMessage"].get("msg", "Unknown error")}
        
        return data.get("WhoisRecord", {})

    except requests.exceptions.RequestException as e:
        return {"error": f"Terjadi kesalahan koneksi: {e}"}
