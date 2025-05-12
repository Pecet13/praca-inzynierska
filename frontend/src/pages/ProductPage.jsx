import React, { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import api from "../api";
import placeholder from "../assets/placeholder.png";
import "../styles/ProductPage.css";
import "../styles/Button.css";

function ProductPage() {
    const { id } = useParams();
    const { isLoggedIn } = useContext(AuthContext);
    const [product, setProduct] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        getProduct();
    }, [id]);

    const getProduct = () => {
        api.get(`/api/products/${id}/`)
            .then((res) => {
                setProduct(res.data);
            })
            .catch((err) => {
                console.error(err);
            });
    };

    // Don't render if product is null
    if (!product) return null;

    return (
        <div className="product-wrapper">
            <h1>{product.name}</h1>
            <div className="product-details">
                <img
                    className="product-details-image"
                    src={product.image_url ? product.image_url : placeholder}
                    alt={product.name}
                />
                <div className="product-description">
                    <h2>Description</h2>
                    <p>{product.description}</p>
                </div>
            </div>
            {isLoggedIn && (
                <div>
                    <button
                        className="button"
                        onClick={() => {
                            navigate(`/products/${id}/review`);
                        }}
                    >
                        Add review
                    </button>
                </div>
            )}
        </div>
    );
}

export default ProductPage;
