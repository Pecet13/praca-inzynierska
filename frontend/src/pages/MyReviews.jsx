import { useState, useEffect } from "react";
import api from "../api";
import { Link, useNavigate } from "react-router-dom";
import placeholder from "../assets/placeholder.png";
import "../styles/MyReviews.css";
import "../styles/Home.css";
import "../styles/Button.css";

function MyReviews() {
    const [products, setProducts] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        getProducts();
    }, []);

    const getProducts = () => {
        api.get("/api/my-reviews/")
            .then((res) => {
                setProducts(res.data);
            })
            .catch((err) => {
                console.error(err);
            });
    };

    const deleteReview = (productId) => {
        api.delete(`/api/products/${productId}/review/`)
            .then((res) => {
                if (res.status === 204) alert("Review deleted!");
                else alert("Failed to delete review.");
                getProducts(); // Refresh the list after deletion
            })
            .catch((err) => {
                console.error(err);
            });
    }

    return (
        <div className="home-wrapper">
            <h1 className="h1">My reviews</h1>
            <div className="product-list">
                {products.map((product) => (
                    <div key={product.id} className="product">
                        <div className="product-left">
                            <img
                                className="product-image"
                                src={
                                    product.image_url
                                        ? product.image_url
                                        : placeholder
                                }
                                alt={product.name}
                            />
                            <Link
                                to={`/products/${product.id}`}
                                className="product-name"
                            >
                                {product.name}
                            </Link>
                        </div>
                        <div className="product-right">
                                <div>
                                    <button
                                        className="button button-primary"
                                        type="button"
                                        onClick={() => {
                                            navigate(
                                                `/products/${product.id}/review`
                                            );
                                        }}
                                    >
                                        Edit review
                                    </button>
                                    <button
                                        className="button button-secondary"
                                        type="button"
                                        onClick={() => {
                                            deleteReview(product.id);
                                        }}
                                    >
                                        Delete review
                                    </button>
                                </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default MyReviews;
