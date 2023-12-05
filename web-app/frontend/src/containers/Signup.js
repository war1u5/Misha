import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { signup } from "../actions/auth";

const Signup = ({ signup, isAuthenticated }) => {
    const [accountCreated, setAccountCreated] = useState(false);
    const [passwordsMatch, setPasswordsMatch] = useState(true);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        re_password: ''
    });

    const { first_name, last_name, email, password, re_password } = formData;
    const navigate = useNavigate();

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onBlur = e => {
        if (e.target.name === 'email') {
            const [username, domain] = e.target.value.split('@');
            if (domain === 'gmail.com') {
                const [firstName, lastName] = username.split('.');
                setFormData({ ...formData, first_name: firstName, last_name: lastName });
            }
        } else if (e.target.name === 're_password') {
            setPasswordsMatch(password === e.target.value);
        }
    };

    const onSubmit = e => {
        e.preventDefault();

        if (password === re_password) {
            signup(first_name, last_name, email, password, re_password);
            setAccountCreated(true);
        } else {
            setPasswordsMatch(false);
        }
    };

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/');
        }
        if (accountCreated) {
            navigate('/login');
        }
    }, [isAuthenticated, accountCreated]);

    return(
        <div className='container mt-5 ' style={{ height: '75.6vh' }}>
            <h1>Sign Up</h1>
            <p>Create your Account</p>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group mb-3'>
                    <input
                        className='form-control'
                        type='email'
                        placeholder='Email'
                        name='email'
                        value={email}
                        onChange={e => onChange(e)}
                        onBlur={e => onBlur(e)}
                        required
                    />
                </div>
                <div className='form-group mb-3'>
                    <input
                        className='form-control'
                        type='text'
                        placeholder='First Name'
                        name='first_name'
                        value={first_name}
                        readOnly
                    />
                </div>
                <div className='form-group mb-3'>
                    <input
                        className='form-control'
                        type='text'
                        placeholder='Last Name'
                        name='last_name'
                        value={last_name}
                        readOnly
                    />
                </div>
                <div className='form-group mb-3'>
                    <input
                        className={`form-control ${!passwordsMatch ? 'is-invalid' : ''}`}
                        type='password'
                        placeholder='Password'
                        name='password'
                        value={password}
                        onChange={e => onChange(e)}
                        minLength='6'
                        required
                    />
                </div>
                <div className='form-group mb-3'>
                    <input
                        className={`form-control ${!passwordsMatch ? 'is-invalid' : ''}`}
                        type='password'
                        placeholder='Confirm Password'
                        name='re_password'
                        value={re_password}
                        onChange={e => onChange(e)}
                        onBlur={e => onBlur(e)}
                        minLength='6'
                        required
                    />
                    {!passwordsMatch && <div className="invalid-feedback">Passwords do not match.</div>}
                </div>
                <button className='btn btn-primary' type='submit'>Register</button>
            </form>
            <p className='mt-3'>
                Already have an account? <Link to='/login'>Sign In</Link>
            </p>
        </div>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});
export default connect(mapStateToProps, { signup })(Signup);
