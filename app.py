from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

from api.virustotal import check_virustotal
from api.whois import get_whois_data
from api.geolocation import get_ip_geolocation
from database import init_db, save_search_history, get_search_history

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='static')

# Load variables from .env
app.secret_key = os.getenv('SECRET_KEY') or 'your_secret_key_default'
USERNAME = os.getenv('APP_USERNAME')
PASSWORD = os.getenv('APP_PASSWORD')

# Initialize the database
init_db()

@app.after_request
def add_header(response):
    """
    Add headers to prevent caching.
    """
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    return response

@app.route('/', methods=['GET'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    history = get_search_history(limit=5)
    return render_template('index.html', history=history)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/check', methods=['POST'])
def check():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    url_to_check = request.form['url']
    if not url_to_check:
        flash('URL tidak boleh kosong!', 'warning')
        return redirect(url_for('index'))

    # Call all APIs
    vt_results = check_virustotal(url_to_check)
    domain_name = url_to_check.split("://")[-1].split("/")[0]
    whois_results = get_whois_data(domain_name)
    geo_results = get_ip_geolocation(domain_name)

    # Save history to SQLite database
    if vt_results and not vt_results.get('error'):
        vt_summary = vt_results.get('last_analysis_stats', {})
        whois_registrar = whois_results.get('registrarName', 'N/A')
        save_search_history(url_to_check, vt_summary, whois_registrar)
    
    # Process data for display
    if vt_results and 'last_analysis_date' in vt_results:
        timestamp = vt_results['last_analysis_date']
        dt_object = datetime.fromtimestamp(timestamp, timezone.utc)
        vt_results['last_analysis_date_human'] = dt_object.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    gsb_results = None
    
    return render_template(
        'results.html', 
        url=url_to_check, 
        vt_results=vt_results, 
        whois_results=whois_results,
        geo_results=geo_results,
        gsb_results=gsb_results
    )


if __name__ == '__main__':
    # PERUBAHAN DI SINI
    app.run(debug=True, port=11005)
