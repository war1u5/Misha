// Create a new WebSocket connection to the server
const socket = new WebSocket('ws://localhost:3000');

// Connection opened
socket.addEventListener('open', (event) => {
  socket.send('Hello Server!');
});

// Listen for messages from the server
socket.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  console.log('Received data from server: ', data);

  // Display the data in a div
  const dataDiv = document.getElementById('data');
  dataDiv.textContent = JSON.stringify(data, null, 2);
});
