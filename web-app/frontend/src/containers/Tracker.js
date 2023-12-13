import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, Popup, LayersControl } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.webpack.css';
import 'leaflet-defaulticon-compatibility';


let helloCount = 0;

const generateRandomData = () => {
  const lat = Math.random() * 18 - 9; // Latitude: -90 to 90
  const lon = Math.random() * 36 - 18; // Longitude: -180 to 180
  const recordedTime = new Date().toISOString();
  const node_id = Math.floor(Math.random() * 1000); // Random node_id from 0 to 999
  const hello = helloCount++;

  return {
    Lat: lat,
    Lng: lon,
    time: recordedTime,
    worker_id: node_id,
    hello: hello,
  };
};

const Tracker = () => {
  const [points, setPoints] = useState([]);
  const [fetching, setFetching] = useState(false);
  const mapRef = useRef(null);

  const fetchData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/gps-data');

    if (response.data.length === 0) {
      console.log('No data received');
      return;
    }

    console.log('Fetched data:', response.data[0]);

    const lat = response.data[0].Lat;
    const lon = response.data[0].Lng;
    const recordedTime = response.data[0].time;
    const node_id = response.data[0].worker_id;
    const count = response.data[0].hello;

    // const randomData = generateRandomData();
    //
    // const lat = randomData.Lat;
    // const lon = randomData.Lng;
    // const recordedTime = randomData.time;
    // const node_id = randomData.worker_id;
    // const count = randomData.hello;

    console.log("Lat: ", lat);
    console.log("Lon: ", lon);
    console.log("time: ", recordedTime);

    setPoints(prevPoints => [
      ...prevPoints,
      {
        Lat: lat,
        Lng: lon,
        time: recordedTime,
        worker_id: node_id,
        packet: count
      },
    ]);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

  useEffect(() => {
    let intervalId;

    if (fetching) {
      intervalId = setInterval(fetchData, 1000);
    }

    return () => clearInterval(intervalId);
  }, [fetching]);

  useEffect(() => {
    if (mapRef.current && points.length > 0) {
      const latestPoint = points[points.length - 1];
      mapRef.current.setView([latestPoint.Lat, latestPoint.Lng], mapRef.current.getZoom());
    }
  }, [points]);

  const handleStart = () => {
    setFetching(true);
  };

  const handleStop = () => {
    setFetching(false);
  };

  const clearMap = () => {
    setPoints([]);
  };

  return (
    <div className='container-fluid text-center'>
      <div className="row">
        <div className="col">
          <div className="d-grid gap-2 mt-5">
            <button className="btn btn-dark" type="button" onClick={handleStart}>Start</button>
            <button className="btn btn-dark" type="button" onClick={handleStop}>Stop</button>
            <button className="btn btn-danger" type="button" onClick={clearMap}>Clear Map</button>
          </div>
        </div>
        <div className="col-10">
          <div className="container-fluid mt-5">
            <MapContainer center={[45, 12]} zoom={4} style={{ height: "75.6vh", width: "100%" }} ref={mapRef}>
              <LayersControl position="topright">
                <LayersControl.BaseLayer checked name="OpenStreetMap">
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='© <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                  />
                </LayersControl.BaseLayer>
                <LayersControl.BaseLayer name="Satellite View">
                  <TileLayer
                    url='https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
                    maxZoom={20}
                    subdomains={['mt0','mt1','mt2','mt3']}
                  />
                </LayersControl.BaseLayer>
              </LayersControl>
              {points.map(point => (
                <Marker key={`${point.time}-${point.packet}`} position={[point.Lat, point.Lng]}>
                  <Popup>
                    <p>{`Time: ${new Date(point.time).toLocaleString()}`}</p>
                    <p>{`Node ID: ${point.worker_id}`}</p>
                    <p>{`Lat: ${point.Lat}`}</p>
                    <p>{`Lng: ${point.Lng}`}</p>
                    <p>{`Packet: ${point.packet}`}</p>
                  </Popup>
                </Marker>
              ))}
              {points.length > 1 && (
                <Polyline positions={points.map(point => [point.Lat, point.Lng])} color="red" />
              )}
            </MapContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tracker;
