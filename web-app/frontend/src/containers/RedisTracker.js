import React, { useEffect, useState, useRef } from 'react';
import {MapContainer, TileLayer, Marker, Polyline, Popup, LayersControl} from 'react-leaflet';
import useWebSocket from 'react-use-websocket';
import 'leaflet/dist/leaflet.css';
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.webpack.css';
import 'leaflet-defaulticon-compatibility';

const RedisTracker = () => {
  const [points, setPoints] = useState([]);
  const mapRef = useRef(null);

  const { sendJsonMessage, lastJsonMessage } = useWebSocket('ws://127.0.0.1:8001/ws');

  useEffect(() => {
    if (lastJsonMessage) {
      const data = lastJsonMessage;
      if (data.Lat && data.Lng) {
        setPoints(prevPoints => [
          ...prevPoints,
          {
            Lat: data.Lat,
            Lng: data.Lng,
            time: Date.now(),
            worker_id: data.worker_id,
            packet: data.hello
          },
        ]);
      }
    }
  }, [lastJsonMessage]);

  useEffect(() => {
    if (mapRef.current && points.length > 0) {
      const latestPoint = points[points.length - 1];
      if (latestPoint.Lat && latestPoint.Lng) {
        mapRef.current.setView([latestPoint.Lat, latestPoint.Lng], mapRef.current.getZoom());
      }
    }
  }, [points]);

  return (
    <div className='container-fluid text-center'>
      <div className="row">
        <div className="col">
          <div className="d-grid gap-2 mt-5">
            <button className="btn btn-dark" type="button" onClick={() => sendJsonMessage({ action: 'start' })}>Start</button>
            <button className="btn btn-dark" type="button" onClick={() => sendJsonMessage({ action: 'stop' })}>Stop</button>
            <button className="btn btn-danger" type="button" onClick={() => setPoints([])}>Clear Map</button>
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

export default RedisTracker;
