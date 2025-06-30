import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../styles/Navbar.css";

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
            <div className="navbar-left">
                <Link to="/" className="nav-link strong">Home</Link>
                <Link to="/ranking" className="nav-link">Ranking</Link>
                <Link to="/charts" className="nav-link">Charts</Link>
                {isLoggedIn && (
                    <Link to="/my-reviews" className="nav-link">My reviews</Link>
                )}
            </div>
            <div className="navbar-right">
                {isLoggedIn ? (
                    <>
                        <span className="nav-link" onClick={handleLogout}>
                            Log out
                        </span>
                    </>
                ) : (
                    <span className="nav-link" onClick={handleLogin}>
                        Log in
                    </span>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
