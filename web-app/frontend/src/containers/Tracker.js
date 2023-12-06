import React, { useEffect, useState } from 'react';
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';
import axios from 'axios';

const Tracker = () => {
  const [points, setPoints] = useState([]);
  const [fetching, setFetching] = useState(false);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/gps-data');
      console.log(response.data);
      setPoints(response.data);
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

  const handleStart = () => {
    setFetching(true);
  };

  const handleStop = () => {
    setFetching(false);
  };

  return (
    <div className='container-fluid text-center'>
      <div className="row">
        <div className="col">
          <div className="d-grid gap-2 mt-5">
            <button className="btn btn-dark " type="button" onClick={handleStart}>Start</button>
            <button className="btn btn-dark" type="button" onClick={handleStop}>Stop</button>
          </div>
        </div>
        <div className="col-10">
          <div className="container-fluid mt-5">
            <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: "75.6vh", width: "100%" }}>
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
              />
              {points.map(point => (
                <Marker key={point.time} position={[point.Lat, point.Lng]}>
                  {/* You can customize the marker as needed */}
                </Marker>
              ))}
              {points.length > 1 && (
                <Polyline positions={points.map(point => [point.Lat, point.Lng])} color="blue" />
              )}
            </MapContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tracker;
