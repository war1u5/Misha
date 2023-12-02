import React, { useState, useEffect } from 'react';
import Globe from 'react-globe.gl';
import * as THREE from 'three';
import * as topojson from 'topojson-client';

const World = () => {
  const [landPolygons, setLandPolygons] = useState([]);

  useEffect(() => {
    fetch('https://unpkg.com/world-atlas/land-110m.json')
      .then((res) => res.json())
      .then((landTopo) => {
        setLandPolygons(topojson.feature(landTopo, landTopo.objects.land).features);
      });
  }, []);

  const polygonsMaterial = new THREE.MeshLambertMaterial({
    color: 'darkslategrey',
    side: THREE.DoubleSide,
  });

  return (
    <Globe
      backgroundColor="rgba(0,0,0,0)"
      showGlobe={false}
      showAtmosphere={false}
      polygonsData={landPolygons}
      polygonCapMaterial={polygonsMaterial}
      polygonSideColor={() => 'rgba(0, 0, 0, 0)'}
    />

  );
};

export default World;
