const express = require('express');
const Influx = require('influx');
const WebSocket = require('ws');
const http = require('http');
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const influx = new Influx.InfluxDB({
  host: '127.0.0.1',
  database: 'main_storage',
  port: 8086,
  username: 'warius',
  password: '12345678',
  schema: [
    {
      measurement: 'kafka_consumer',
      fields: {
        lat: Influx.FieldType.FLOAT,
        lon: Influx.FieldType.FLOAT
      },
      tags: ['device_id']
    }
  ]
});

// Serve static files from the current directory
app.use(express.static(path.join(__dirname, '../frontend')));

wss.on('connection', ws => {
  console.log('Client connected');

  setInterval(async () => {
    try {
      const result = await influx.query(`
        select * from kafka_consumer
        order by time desc
        limit 1
      `);

      ws.send(JSON.stringify(result));
    } catch (error) {
      console.error(`Error querying data from InfluxDB! ${error.stack}`);
    }
  }, 1000);
});

server.listen(3000, () => {
  console.log(`Server listening at http://localhost:3000`);
});
