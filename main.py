# main.py
import subprocess
import time
from ping3 import ping
from speedtest import Speedtest
import sqlite3
import datetime

# Start the Flask server as a separate process
subprocess.Popen(['python', 'server.py'])

# Database setup
conn = sqlite3.connect('internet_speeds.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS speeds (
        date_time TEXT,
        ping_ms REAL,
        download_speed REAL,
        upload_speed REAL
    )
''')
conn.commit()


def check_internet_speeds():
    response_time = ping('google.com')
    ping_ms = response_time * 1000 if response_time else None

    st = Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000

    now = datetime.datetime.now().isoformat()

    c.execute('''
        INSERT INTO speeds (date_time, ping_ms, download_speed, upload_speed)
        VALUES (?, ?, ?, ?)
    ''', (now, ping_ms, download_speed, upload_speed))
    conn.commit()


if __name__ == "__main__":
    while True:
        check_internet_speeds()
        time.sleep(60)  # Sleep for one minute
