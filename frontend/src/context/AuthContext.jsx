import { createContext, useEffect, useState } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [isLoggedIn, setIsLoggedIn] = useState(
        !!localStorage.getItem("access_token")
    );

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        setIsLoggedIn(!!token);
    }, []);

    const login = (access, refresh) => {
        localStorage.setItem("access_token", access);
        localStorage.setItem("refresh_token", refresh);
        setIsLoggedIn(true);
    };

    const logout = () => {
        localStorage.clear();
        setIsLoggedIn(false);
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}
