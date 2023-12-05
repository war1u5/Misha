import React, { useEffect, useState } from 'react';
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer } from 'react-leaflet';

const Tracker = () => (
    <div className='container-fluid text-center'>
        <div className="row">
            <div className="col">
                <div className="d-grid gap-2 mt-5">
                    <button className="btn btn-dark " type="button">Button</button>
                    <button className="btn btn-dark" type="button">Button</button>
                    <button className="btn btn-dark" type="button">Button</button>
                </div>
            </div>
            <div className="col-10">
                <div className="container-fluid mt-5">
                    <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: "75.6vh", width: "100%" }}>
                    <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    />
                </MapContainer>
                </div>
            </div>
        </div>
    </div>
);


export default Tracker;
