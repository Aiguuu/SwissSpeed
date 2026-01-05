from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")


def init_db():
	created = not os.path.exists(DB_PATH)
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()
	cur.execute(
		"""
		CREATE TABLE IF NOT EXISTS locations (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			lat REAL NOT NULL,
			lon REAL NOT NULL,
			info TEXT
		)
		"""
	)
	if created:
		cur.executemany(
			"INSERT INTO locations (name, lat, lon, info) VALUES (?, ?, ?, ?)",
			[
				("Campus A", 48.1351, 11.5820, "Main campus"),
				("Library", 48.1372, 11.5756, "Open 9-18"),
				("Lab", 48.133, 11.58, "CS Lab")
			],
		)
	conn.commit()
	conn.close()


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/api/locations")
def api_locations():
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()
	cur.execute("SELECT id, name, lat, lon, info FROM locations")
	rows = cur.fetchall()
	conn.close()
	data = [
		{"id": r[0], "name": r[1], "lat": r[2], "lon": r[3], "info": r[4]}
		for r in rows
	]
	return jsonify(data)


def main():
	init_db()
	host = os.getenv("HOST", "127.0.0.1")
	port = int(os.getenv("PORT", "5050"))
	app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
	main()
