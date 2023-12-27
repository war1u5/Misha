import React, { useEffect, useState, createContext } from 'react';
import Navbar from '../components/Navbar';
import Copyrights from '../components/Copyrights';
import { connect } from "react-redux";
import { checkAuthenticated, load_user } from "../actions/auth";

export const ThemeContext = createContext(undefined);

const Layout = ({ checkAuthenticated, load_user, children }) => {
    const [theme, setTheme] = useState('text-bg-light');

    const toggleTheme = () => { // add a function to toggle the theme
        setTheme(theme === 'text-bg-secondary' ? 'text-bg-light' : 'text-bg-secondary');
    };

    useEffect(() => {
        checkAuthenticated();
        load_user();
    }, []);

    return (
        <ThemeContext.Provider value={{ toggleTheme }}>
            <div className={theme + " p-3"}>
                <Navbar />
                {children}
                <Copyrights />
            </div>
        </ThemeContext.Provider>
    );
};

export default connect(null, { checkAuthenticated, load_user })(Layout);