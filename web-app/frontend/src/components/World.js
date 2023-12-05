import React, { useState, useEffect } from 'react';
import Globe from 'react-globe.gl';
import * as THREE from 'three';
import * as topojson from 'topojson-client';
import landData from '../assets/world-110m.json';

const World = () => {
  const [landPolygons, setLandPolygons] = useState([]);
   const [arcsData, setArcsData] = useState([]);

  useEffect(() => {
    setLandPolygons(topojson.feature(landData, landData.objects.land).features);

    const N = 20;
    const newArcsData = [...Array(N).keys()].map(() => ({
      startLat: (Math.random() - 0.5) * 180,
      startLng: (Math.random() - 0.5) * 360,
      endLat: (Math.random() - 0.5) * 180,
      endLng: (Math.random() - 0.5) * 360,
      color: [['red', 'white', 'blue', 'green'][Math.round(Math.random() * 3)], ['red', 'white', 'blue', 'green'][Math.round(Math.random() * 3)]]
    }));
    setArcsData(newArcsData);
  }, []);

  const polygonsMaterial = new THREE.MeshLambertMaterial({
    color: 'black',
    side: THREE.DoubleSide,
  });

  return (
      <div className='container-fluid text-center'>
        <Globe
          backgroundColor='rgba(0,0,0,0)'
          showGlobe={false}
          showAtmosphere={false}
          polygonsData={landPolygons}
          polygonCapMaterial={polygonsMaterial}
          polygonSideColor={() => 'rgba(0, 0, 0, 0)'}
          width='1250'
          height='545'
          animateIn={true}
          arcsData={arcsData}
          arcColor={'color'}
          arcDashLength={() => Math.random()}
          arcDashGap={() => Math.random()}
          arcDashAnimateTime={() => Math.random() * 4000 + 500}
          
        />
      </div>
  );
};

export default World;
