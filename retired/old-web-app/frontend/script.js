let socket = null;
let intervalId = null;

const map = L.map('map').setView([0, 0], 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let polyline = L.polyline([], { color: 'red' }).addTo(map);

document.getElementById('startButton').addEventListener('click', () => {
  socket = new WebSocket('ws://localhost:3000');

  socket.addEventListener('open', (event) => {
    socket.send('Hello Server!');
  });

  socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    console.log('Received data from server: ', data);

//    const lat = data[0].Lat; /* + Math.random() * 20 - 10;*/
//    const lon = data[0].Lng; /* + Math.random() * 30 - 20;*/
//    const device = data[0].worker_id;

    const lat = 40 + data[0].Lat + Math.random() * 2 - 10;
    const lon = 50 + data[0].Lng + Math.random() * 3 - 20;
    const device = data[0].worker_id;

    console.log(lat);
    console.log(lon);
    console.log(device);

    const latLng = L.latLng(lat, lon);
    polyline.addLatLng(latLng);
    map.panTo(latLng);
  });

  intervalId = setInterval(() => {
    socket.send('Requesting data');
  }, 1000);
});

document.getElementById('stopButton').addEventListener('click', () => {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }

  if (socket) {
    socket.close();
    socket = null;
  }
});

document.getElementById('clearButton').addEventListener('click', () => {
  map.removeLayer(polyline);

  polyline = L.polyline([], { color: 'red' }).addTo(map);
});
