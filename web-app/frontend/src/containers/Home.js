import React from 'react';
import World from '../components/World'
import Globe from "../components/Globe";

const Home = () => (

    <div className='container' style={{ height: '75.7vh' }}>
        <div className="jumbotron mt-5 ">
            <h1 className="display-4">Hello there! This is M.I.S.H.A.</h1>
            <p className="lead">Military Intelligence Surveillance and Hazard Assessment</p>
            <hr className="my-4" />
        </div>
        <div className='container-fluid text-center'>
            <World />
        </div>
    </div>
);

export default Home;