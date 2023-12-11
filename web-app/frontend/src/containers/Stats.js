import React, { useState } from 'react';

const Stats = () => {
    const [url, setUrl] = useState('http://localhost:3000/d/c85c31ec-f454-42d8-85a2-669f8ea44c00/gps?orgId=1&refresh=5s');

    return (
        <div className='container-fluid text-center mt-5'>
            <div style={{ display: 'flex' }}>
                <iframe src={url} width="100%" height="655"></iframe>
            </div>
            <div className="btn-group" role="group" style={{ marginRight: '20px' }}>
                <button className='btn btn-dark mt-2' onClick={() => setUrl('http://localhost:3000/d/c85c31ec-f454-42d8-85a2-669f8ea44c00/gps?orgId=1&refresh=5s')}>Signal Strength</button>
                <button className='btn btn-dark mt-2' onClick={() => setUrl('http://localhost:3000/d/c812e7d9-5e78-4b6e-901c-6d0688e16229/satellites-connected?orgId=1&refresh=5s')}>Satellites Connected</button>
                <button className='btn btn-dark mt-2' onClick={() => setUrl('url3')}>Button 3</button>
            </div>
        </div>
    );
};

export default Stats;
