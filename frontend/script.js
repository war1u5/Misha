const socket = new WebSocket('ws://localhost:3000');

const map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
const polyline = L.polyline([], { color: 'red' }).addTo(map);

socket.addEventListener('open', (event) => {
  socket.send('Hello Server!');
});

socket.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  console.log('Received data from server: ', data);

  const lat = data[0].Lat + Math.random() * 180 - 90;
  const lon = data[0].Lng + Math.random() * 360 - 180;
  console.log(lat)
  console.log(lon)

  const latLng = L.latLng(lat, lon);
  polyline.addLatLng(latLng);
  map.panTo(latLng);
});
