import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Navbar.css";
import { AuthContext } from "../context/AuthContext";

const Navbar = () => {
    const { isLoggedIn, logout } = useContext(AuthContext);
    const navigate = useNavigate();
    const handleLogout = () => {
        logout();
        navigate("/login");
    };
    const handleLogin = () => {
        navigate("/login");
    };

    return (
        <nav className="navbar">
            <div>
                <Link to="/">Home</Link>
            </div>
            {isLoggedIn && <Link to="/my-reviews">My reviews</Link>}
            <Link to="/ranking">Ranking</Link>
            <Link to="/charts">Charts</Link>
            {isLoggedIn ? (
                <span className="logout-button" onClick={handleLogout}>
                    Logout
                </span>
            ) : (
                <span className="login-button" onClick={handleLogin}>
                    Login
                </span>
            )}
        </nav>
    );
};

export default Navbar;
