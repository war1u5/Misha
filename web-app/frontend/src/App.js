import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from './containers/Home';
import Login from './containers/Login';
import Signup from './containers/Signup';
import Activate from './containers/Activate';
import ResetPassword from './containers/ResetPassword';
import ResetPasswordConfirm from './containers/ResetPasswordConfirm';
import Tracker from './containers/Tracker';
import Stats from "./containers/Stats";

import {Provider} from "react-redux";
import store from './store';

import Layout from './hocs/Layout';
import PrivateRoute from "./utils/PrivateRoute";


const App = () => (
    <Provider store={store}>
        <Router>
            <Layout>
                <Routes>
                    <Route path='/' element={<Home />} />
                    <Route path='/login' element={<Login />} />
                    <Route path='/signup' element={<Signup />} />
                    <Route path='/activate/:uid/:token' element={<Activate />} />
                    <Route path='/reset-password' element={<ResetPassword />} />
                    <Route path='/password/reset/confirm/:uid/:token' element={<ResetPasswordConfirm />} />
                    <Route element={<PrivateRoute/>}>
                        <Route path='/tracker' element={<Tracker />}/>
                        <Route path='/stats' element={<Stats />} />
                    </Route>
                </Routes>
            </Layout>
        </Router>
    </Provider>
);

export default App;
