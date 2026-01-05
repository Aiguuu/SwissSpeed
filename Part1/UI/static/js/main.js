const map = L.map('map').setView([48.1351, 11.5820], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

fetch('/api/locations')
  .then(r => r.json())
  .then(data => {
    data.forEach(item => {
      const marker = L.marker([item.lat, item.lon]).addTo(map);
      const content = `<strong>${item.name}</strong><br/>${item.info ?? ''}`;
      marker.bindPopup(content);
    });
  })
  .catch(err => console.error('Failed to load locations', err));