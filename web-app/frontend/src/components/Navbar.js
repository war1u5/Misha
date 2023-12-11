import React, { Fragment, useContext } from 'react';
import { Link } from "react-router-dom";
import { logout } from "../actions/auth";
import { connect } from "react-redux";
import { ThemeContext } from '../hocs/Layout';

const Navbar = ({ logout, isAuthenticated }) => {
    const { toggleTheme } = useContext(ThemeContext);
    const guestLinks = () => (
        <Fragment>
            <li className="nav-item">
                <Link className="nav-link" to="/login">Login</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link" to="/signup">Sign Up</Link>
            </li>
        </Fragment>
    );

    const authLinks = () => (
        <Fragment>
            <li className="nav-item">
                <Link className="nav-link" to="/tracker">Tracker</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link" to="/stats">Stats</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link" to="/redis">Redis</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link" to="/reports">Reports</Link>
            </li>
            <li className="nav-item">
                <a className="nav-link" href="#!" onClick={logout}>Logout</a>
            </li>
        </Fragment>
    );

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <Link className="navbar-brand" style={{ paddingLeft: '1rem' }} to="/">M.I.S.H.A.</Link>
          <button
              className="navbar-toggler"
              type="button"
              data-toggle="collapse"
              data-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="nav nav-underline">
                <li className="nav-item active">
                    <Link className="nav-link" to="/">Home</Link>
                </li>
                {isAuthenticated ? authLinks() : guestLinks()}
            </ul>
            <ul className="nav justify-content-end">
                <li className="nav-item active">
                    <button className="nav-link" onClick={ toggleTheme }>
                        Toggle Theme
                    </button>
                </li>
            </ul>
          </div>
        </nav>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { logout })(Navbar);