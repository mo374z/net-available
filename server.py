# server.py
from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('internet_speeds.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/api/stats')
def stats():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM speeds ORDER BY date_time DESC LIMIT 1')
    latest_stats = cur.fetchone()
    conn.close()
    return jsonify(dict(latest_stats))


@app.route('/api/downtimes')
def downtimes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM speeds WHERE ping_ms IS NULL')
    downtimes = cur.fetchall()
    conn.close()
    return jsonify([dict(dt) for dt in downtimes])


@app.route('/api/historical')
def historical():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM speeds ORDER BY date_time DESC LIMIT 60')
    data = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])


@app.route('/api/availability')
def availability():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as total FROM speeds')
    total_entries = cur.fetchone()['total']
    cur.execute('SELECT COUNT(*) as up FROM speeds WHERE ping_ms IS NOT NULL')
    up_entries = cur.fetchone()['up']
    conn.close()
    if total_entries > 0:
        availability = (up_entries / total_entries) * 100
    else:
        0
    return jsonify({'availability': availability})


if __name__ == '__main__':
    app.run(debug=True)
