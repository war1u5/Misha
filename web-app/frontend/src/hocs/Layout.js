import React, { useEffect, useState, createContext } from 'react';
import Navbar from '../components/Navbar';
import { connect } from "react-redux";
import { checkAuthenticated, load_user } from "../actions/auth";

export const ThemeContext = createContext();

const Layout = ({ checkAuthenticated, load_user, children }) => {
    const [theme, setTheme] = useState('text-bg-dark');

    const toggleTheme = () => { // add a function to toggle the theme
        setTheme(theme === 'text-bg-dark' ? 'text-bg-light' : 'text-bg-dark');
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
            </div>
        </ThemeContext.Provider>
    );
};

export default connect(null, { checkAuthenticated, load_user })(Layout);