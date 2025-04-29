import react from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import Ranking from "./pages/Ranking";
import Charts from "./pages/Charts";
import MyReviews from "./pages/MyReviews";
import ProductPage from "./pages/ProductPage";
import { AuthProvider } from "./context/AuthContext.jsx";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/Navbar";
import "./styles/App.css";

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Navbar />
                <div className="app-container">
                    <Routes>
                        <Route
                            path="/my-reviews"
                            element={
                                <ProtectedRoute>
                                    <MyReviews />
                                </ProtectedRoute>
                            }
                        />
                        <Route path="/" element={<Home />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/ranking" element={<Ranking />} />
                        <Route path="/charts" element={<Charts />} />
                        <Route path="/products/:id" element={<ProductPage />} />
                        <Route path="*" element={<NotFound />} />
                    </Routes>
                </div>
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;
