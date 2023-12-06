import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, Popup } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.webpack.css'; // Re-uses images from ~leaflet package
import * as L from 'leaflet';
import 'leaflet-defaulticon-compatibility';

const generateRandomCoordinates = () => {
  return Math.random() % 30;
};

const Tracker = () => {
  const [points, setPoints] = useState([]);
  const [fetching, setFetching] = useState(false);
  const mapRef = useRef(null);

  const fetchData = async () => {
    const response = await axios.get('http://127.0.0.1:5000/api/gps-data');

    console.log('Fetched data:', response.data[0]);

    const randomLatOffset = generateRandomCoordinates();
    const randomLngOffset = generateRandomCoordinates();

    const lat = response.data[0].Lat;
    const lon = response.data[0].Lng;
    const recordedTime = response.data[0].time;
    const node_id = response.data[0].worker_id;

    console.log("Lat: ", lat);
    console.log("Lon: ", lon);
    console.log("time: ", recordedTime);

    const testLat = lat + randomLatOffset;
    const testLon = lon + randomLngOffset;

    setPoints(prevPoints => [
        ...prevPoints,
        {
          Lat: testLat,
          Lng: testLon,
          time: recordedTime,
          worker_id: node_id
        },
      ]);
  };

  useEffect(() => {
    let intervalId;

    if (fetching) {
      intervalId = setInterval(fetchData, 2000);
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
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='© <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
              />
              {points.map(point => (
                <Marker key={point.time} position={[point.Lat, point.Lng]}>
                  <Popup>
                    <p>{`Time: ${new Date(point.time).toLocaleString()}`}</p>
                    <p>{`Node ID: ${point.worker_id}`}</p>
                    <p>{`Lat: ${point.Lat}`}</p>
                    <p>{`Lng: ${point.Lng}`}</p>
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
