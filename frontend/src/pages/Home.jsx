import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import api from "../api";
import placeholder from "../assets/placeholder.png";
import "../styles/Home.css";
import "../styles/Button.css";

function Home() {
    const [products, setProducts] = useState([]);
    const [search, setSearch] = useState("");
    const { isLoggedIn } = useContext(AuthContext);

    useEffect(() => {
        getProducts();
    }, []);

    const getProducts = () => {
        api.get("/api/products/")
            .then((res) => res.data)
            .then((data) => {
                setProducts(data);
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
                            <h2>{product.name}</h2>
                        </div>
                        <div className="product-right">
                            {isLoggedIn && (
                                <div>
                                    <button className="button">
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
