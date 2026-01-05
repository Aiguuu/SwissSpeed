# Map UI with Flask + Leaflet

This app displays an OpenStreetMap-based map and overlays location data from a local SQLite database via a Flask API.

## Quick Start

1. Create/activate your virtual environment.
2. Install dependencies.
3. Run the app.

### One-liner (Windows)

```powershell
./scripts/setup.ps1 -Run
```

### One-liner (Linux/Mac)

```bash
bash scripts/setup.sh --run
```

### Manual (Windows)

```bash
# From the project folder
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python UI.py
```

Open http://127.0.0.1:5050 in your browser.

### Manual (Linux/Mac)

```bash
# From the project folder
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Optionally expose outside the VM
HOST=0.0.0.0 PORT=5050 python UI.py
```

Open http://127.0.0.1:5050 inside the VM, or http://<vm-ip>:5050 from the host if you set `HOST=0.0.0.0` and your VM/network allows it.

## Data

On first run, a `data.db` file is created with sample rows in a `locations` table. Edit the table to add your own points (columns: `name`, `lat`, `lon`, `info`).

## Customize

- Update the default map center/zoom in `static/js/main.js`.
- Add more fields to the popup in `static/js/main.js` and the API in `UI.py`.
  
Note: The app fetches Leaflet and map tiles from the internet (CDN/OpenStreetMap). If you're offline, vendor Leaflet locally and point the tile layer to an accessible server.

## VM/Networking

- To access the app from outside the VM, run with `HOST=0.0.0.0` and ensure port `5050` is allowed by your VM firewall and either bridged networking or NAT port forwarding is configured.
- Keep `debug=True` for development only. For production, use a WSGI server and disable debug.

## Optional: Install as a CLI

After cloning, you can install the app as a console command named `map-ui`:

```bash
python -m pip install -e .
# then run
map-ui
```