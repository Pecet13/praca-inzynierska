import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import api from "../api";
import placeholder from "../assets/placeholder.png";
import "../styles/Home.css";
import "../styles/Button.css";
import { Link, useNavigate } from "react-router-dom";

function Home() {
    const [products, setProducts] = useState([]);
    const [search, setSearch] = useState("");
    const { isLoggedIn } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        getProducts();
    }, []);

    const getProducts = () => {
        api.get("/api/products/")
            .then((res) => {
                setProducts(res.data);
            })
            .catch((err) => {
                console.error(err);
            });
    };

    const handleSearch = (e) => {
        setSearch(e.target.value);
    };

    const filteredProducts = products.filter((product) =>
        product.name.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="home-wrapper">
            <input
                type="text"
                className="search-bar"
                value={search}
                onChange={handleSearch}
                placeholder="Search"
            ></input>
            <div className="product-list">
                {filteredProducts.map((product) => (
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
                            {isLoggedIn && (
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
                                        Add review
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Home;
