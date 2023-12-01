import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from './containers/Home';
import Login from './containers/Login';
import Signup from './containers/Signup';
import Activate from './containers/Activate';
import ResetPassword from './containers/ResetPassword';
import ResetPasswordConfirm from './containers/ResetPasswordConfirm';

import Layout from './hocs/Layout';

const App = () => (
    <Router>
        <Layout>
            <Routes>
                <Route path='/' element={<Home />} />
                <Route path='/login' element={<Login />} />
                <Route path='/signup' element={<Signup />} />
                <Route path='/activate/:uid/:token' element={<Activate />} />
                <Route path='/reset-password' element={<ResetPassword />} />
                <Route path='/password/reset/confirm/:uid/:token' element={<ResetPasswordConfirm />} />
            </Routes>
        </Layout>
    </Router>
);

export default App;
