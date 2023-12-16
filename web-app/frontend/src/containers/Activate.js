import React, { useState, useEffect } from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import { connect } from 'react-redux';
import { verify } from "../actions/auth";
import "../styles/Activate.css"

const Activate = ({ verify }) => {
    const navigate = useNavigate();
    const [verified, setVerified] = useState(false);
    const { uid, token } = useParams();

    const verify_account = e => {
        verify(uid, token); // Use uid and token here
        setVerified(true);
    };

    useEffect(() => {
        if (verified) {
            navigate('/');
        }
    }, [verified]);

    return(
        <div className='container'>
            <div className='activation-box'>
                <h1>Verify your Account:</h1>
                <button onClick={verify_account} type='button' className='btn btn-primary verify-button'>
                    Verify
                </button>
            </div>
        </div>
    );
};

export default connect(null, { verify  })(Activate);
