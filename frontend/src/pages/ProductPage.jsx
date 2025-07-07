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
    const [productTypes, setProductTypes] = useState([]);
    const [product, setProduct] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        getProductsTypes();
        getProduct();
    }, [id]);

    const getProductsTypes = () => {
        api.get("/api/product-types/")
            .then((res) => {
                setProductTypes(res.data);
            })
            .catch((err) => {
                console.error(err);
            });
    };

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

    const productType = productTypes.find(
        (type) => type.id === product.product_type
    );

    return (
        <div className="product-wrapper">
            <h1>{product.name}</h1>
            <h2>Product type: {productType.name}</h2>
            <div className="product-details">
                <div className="product-details-image-container">
                    <img
                        className="product-details-image"
                        src={
                            product.image_url ? product.image_url : placeholder
                        }
                        alt={product.name}
                    />
                </div>
                <div className="product-description">
                    <h2>Description</h2>
                    <p>{product.description}</p>
                </div>
            </div>
            {isLoggedIn && (
                <div>
                    <button
                        className="button button-primary"
                        type="button"
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
