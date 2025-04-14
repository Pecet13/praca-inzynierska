import { useState, useContext } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../styles/Form.css";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const navigate = useNavigate();

    const { login } = useContext(AuthContext);

    const name = method === "login" ? "Log in" : "Register";

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (method === "register" && password != confirmPassword) {
            alert("Passwords do not match");
            return;
        }

        try {
            const res = await api.post(route, { username, password });
            if (method === "login") {
                login(res.data.access, res.data.refresh);
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error) {
            alert(error);
        }
    };

    return (
        <form className="form-wrapper" onSubmit={handleSubmit}>
            <h1>{name}</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            {method === "register" && (
                <input
                    className="form-input"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Confirm Password"
                />
            )}
            <button className="form-button" type="submit">
                {name}
            </button>
            {method === "login" && (
                <button
                    className="form-button"
                    type="button"
                    onClick={() => navigate("/register")}
                >
                    Register
                </button>
            )}
        </form>
    );
}

export default Form;
