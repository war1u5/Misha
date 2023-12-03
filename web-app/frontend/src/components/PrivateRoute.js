import React, { useEffect } from 'react';
import { Route, useNavigate } from 'react-router-dom';
import { connect } from 'react-redux';

const PrivateRoute = ({ children, isAuthenticated, ...rest }) => {
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated) {
            navigate('/login');
        }
    }, [isAuthenticated, navigate]);

    return (
        <Route {...rest} element={isAuthenticated ? children : null} />
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps)(PrivateRoute);
