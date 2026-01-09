from flask import Flask, render_template
import plotly.express as px
import sqlite3
from datetime import datetime, timedelta, timezone 

class DashboardServer:
    def __init__(self, db_handler, port=5000):
        self.db_handler = db_handler
        self.app = Flask(__name__)
        self.port = port
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def dashboard():
            data = self._fetch_data()
            plots = self._generate_plots(data)
            return render_template('/home/theobias/SwissSpeed/Part2/Dashboard.html', **plots)

    def _fetch_data(self):
        data = self.db_handler.fetch_all()
        print("Data fetched:", data)
        return data

    def _generate_plots(self, data):
        if not data:
            print("No data to plot!")
            return {'plot1': '', 'plot2': ''}

        # Extract columns
        timestamps = []
        light_flow = []
        heavy_flow = []
        light_speed = []
        heavy_speed = []

        for row in data:
            try:
                # Parse ISO 8601 format and make it timezone-aware
                timestamp_str = row[1]
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                timestamps.append(timestamp)

                light_flow.append(float(row[2]) if row[2] is not None and float(row[2]) >= 0 else None)
                heavy_flow.append(float(row[3]) if row[3] is not None and float(row[3]) >= 0 else None)
                light_speed.append(float(row[4]) if row[4] is not None and float(row[4]) >= 0 else None)
                heavy_speed.append(float(row[5]) if row[5] is not None and float(row[5]) >= 0 else None)
            except (ValueError, TypeError) as e:
                print(f"Error parsing row {row}: {e}")
                continue

        # Get current time in UTC to match the timestamps
        now = datetime.now(timezone.utc)

        # Filter data from the last 24 hours
        filtered_indices = [i for i, ts in enumerate(timestamps) if now - ts <= timedelta(hours=24)]

        # Filter data
        timestamps = [timestamps[i] for i in filtered_indices]
        light_flow = [light_flow[i] for i in filtered_indices]
        heavy_flow = [heavy_flow[i] for i in filtered_indices]
        light_speed = [light_speed[i] for i in filtered_indices]
        heavy_speed = [heavy_speed[i] for i in filtered_indices]

        if not timestamps:
            print("No valid timestamps to plot!")
            return {'plot1': '', 'plot2': ''}

        # Create a DataFrame for Plotly
        import pandas as pd
        df = pd.DataFrame({
            'Timestamp': timestamps,
            'LightFlow': light_flow,
            'HeavyFlow': heavy_flow,
            'LightSpeed': light_speed,
            'HeavySpeed': heavy_speed
        })

        # Remove rows with None values
        df = df.dropna()

        if df.empty:
            print("No valid data to plot after filtering!")
            return {'plot1': '', 'plot2': ''}

        # Plot 1: Flow (LightFlow and HeavyFlow)
        fig1 = px.line(
            df,
            x='Timestamp',
            y=['LightFlow', 'HeavyFlow'],
            title='Measured Traffic Flow (Last Measurements)',
            labels={'value': 'Flow', 'variable': 'Type', 'Timestamp': 'Time'},
        )
        fig1.update_traces(connectgaps=False)
        fig1.update_layout(template="plotly_dark")  # Applique le thème sombre

        # Plot 2: Speed (LightSpeed and HeavySpeed)
        fig2 = px.line(
            df,
            x='Timestamp',
            y=['LightSpeed', 'HeavySpeed'],
            title='Average Measured Traffic Speed (Last Measurements)',
            labels={'value': 'Speed', 'variable': 'Type', 'Timestamp': 'Time'},
        )
        fig2.update_traces(connectgaps=False)
        fig2.update_layout(template="plotly_dark")  # Applique le thème sombre

        return {
            'plot1': fig1.to_html(full_html=False),
            'plot2': fig2.to_html(full_html=False)
        }

        
    def run(self):
        self.app.run(host='0.0.0.0', port=5000, debug=True)
