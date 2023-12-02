import React from 'react';
import World from '../components/World'

const Home = () => (
    <div className='container'>
        <div className="jumbotron mt-5 ">
            <h1 className="display-4">Hello there! This is M.I.S.H.A.</h1>
            <p className="lead">Military Intelligence Surveillance and Hazard Assessment</p>
            <hr className="my-4" />
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative', top: '-150px' }}>
            <World />
        </div>
    </div>
);

export default Home;