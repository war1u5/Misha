import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { login } from "../actions/auth";
import { FaUser, FaLock } from "react-icons/fa";
import "../styles/Login.css"

const Login = ({ login, isAuthenticated }) => {
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [loginError, setLoginError] = useState(null);

    const { email, password } = formData;
    const navigate = useNavigate();

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async (e) => {
        e.preventDefault();
        setFormData({ email: '', password: '' });

        try {
            await login(email, password);
        } catch (err) {
            setLoginError('Invalid credentials. Please try again.');
        }
    };

    const onFormClick = () => {
        setLoginError(null);
    };

    useEffect(() => {
        const handleLoginError = async () => {
            try {
                await login(email, password);
                setLoginError(null);
            } catch (err) {
                setLoginError('Invalid credentials. Please try again.');
            }
        };

        if (isAuthenticated) {
            navigate('/');
        } else if (loginError) {
            handleLoginError();
        }
    }, [isAuthenticated, loginError]);

    return (
        <div className='container mt-5 form-container'>
            <h1>Sign In</h1>
            <p>Sign into your Account</p>
            {loginError && <div className="alert alert-danger">{loginError}</div>}
            <form onSubmit={e => onSubmit(e)} onClick={onFormClick}>
                <div className='form-group mb-3 input-box'>
                    <input
                        className='form-control'
                        type='email'
                        placeholder='Email'
                        name='email'
                        value={email}
                        onChange={e => onChange(e)}
                        required
                    />
                    <FaUser className='icon'/>
                </div>
                <div className='form-group mb-3 input-box'>
                    <input
                        className='form-control'
                        type='password'
                        placeholder='Password'
                        name='password'
                        value={password}
                        onChange={e => onChange(e)}
                        minLength='6'
                        required
                    />
                    <FaLock className='icon'/>
                </div>
                <button className='btn btn-primary' type='submit'>Login</button>
            </form>
            <p className='mt-3'>
                Don't have an account? <Link to='/signup'>Sign Up</Link>
            </p>
            <p className='mt-3'>
                Forgot your password? <Link to='/reset-password'>Reset Password</Link>
            </p>
        </div>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
    loginError: state.auth.payload
});

export default connect(mapStateToProps, { login })(Login);
