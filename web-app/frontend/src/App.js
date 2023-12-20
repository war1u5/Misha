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
import RedisTracker from "./containers/RedisTracker";
import Reports from "./containers/Reports";


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
                        <Route path='/redis' element={<RedisTracker />} />
                        <Route path='/reports' element={<Reports />} />
                    </Route>
                    {/*<Route element={<PrivateRoute requiredPermission="is_commander"/>}>*/}
                    {/*    <Route path='/tracker' element={<Tracker />}/>*/}
                    {/*</Route>*/}
                    {/*<Route element={<PrivateRoute requiredPermission="is_c2operator"/>}>*/}
                    {/*    <Route path='/stats' element={<Stats />} />*/}
                    {/*</Route>*/}
                    {/*<Route element={<PrivateRoute requiredPermission="is_analyst"/>}>*/}
                    {/*    <Route path='/redis' element={<RedisTracker />} />*/}
                    {/*</Route>*/}
                    {/*<Route element={<PrivateRoute requiredPermission="is_agent"/>}>*/}
                    {/*    <Route path='/reports' element={<Reports />} />*/}
                    {/*</Route>*/}
                </Routes>
            </Layout>
        </Router>
    </Provider>
);

export default App;
