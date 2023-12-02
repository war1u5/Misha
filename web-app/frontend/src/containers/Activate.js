import React, { useState, useEffect } from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import { connect } from 'react-redux';
import { verify } from "../actions/auth";

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
            <div
                className='d-flex flex-column justify-content-center align-items-center'
                style={{ marginTop: '200px' }}
            >
                <h1>Verify your Account:</h1>
                <button
                    onClick={verify_account}
                    style={{ marginTop: '50px' }}
                    type='button'
                    className='btn btn-primary'
                >
                    Verify
                </button>
            </div>
        </div>
    );
};

export default connect(null, { verify  })(Activate);
