import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import api from "../api";
import placeholder from "../assets/placeholder.png";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Home.css";
import "../styles/Button.css";

function Home() {
    const [productTypes, setProductTypes] = useState([]);
    const [products, setProducts] = useState([]);
    const [productType, setProductType] = useState(0);
    const [search, setSearch] = useState("");
    const { isLoggedIn } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        getProductsTypes();
        getProducts();
    }, []);

    const getProductsTypes = () => {
        api.get("/api/product-types/")
            .then((res) => {
                setProductTypes(res.data);
            })
            .catch((err) => {
                console.error(err);
            });
    };

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

    const base =
        productType === 0
            ? products
            : products.filter(
                  (product) => product.product_type === productType
              );

    const filteredProducts = base.filter((product) =>
        product.name.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="home-wrapper">
            <div className="home-header">
                <select
                    className="select"
                    value={productType}
                    onChange={(e) => setProductType(Number(e.target.value))}
                >
                    <option value="0">All products</option>
                    {productTypes.map((pt) => (
                        <option key={pt.id} value={pt.id}>
                            {pt.name}
                        </option>
                    ))}
                </select>
                <input
                    type="text"
                    className="search-bar"
                    value={search}
                    onChange={handleSearch}
                    placeholder="Search"
                ></input>
            </div>
            <div className="product-list">
                {filteredProducts.map((product) => (
                    <div key={product.id} className="product">
                        <div className="product-left">
                            <div className="product-image-container">
                                <img
                                    className="product-image"
                                    src={
                                        product.image_url
                                            ? product.image_url
                                            : placeholder
                                    }
                                    alt={product.name}
                                />
                            </div>
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
