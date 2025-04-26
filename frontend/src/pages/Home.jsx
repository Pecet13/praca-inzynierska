import { useState, useEffect } from "react";
import api from "../api";
import Product from "../components/Product";

function Home() {
    const [products, setProducts] = useState([]);

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

    return (
        <div>
            <h1>Home</h1>
            {products.map((product) => (
                <Product key={product.id} product={product} />
            ))}
        </div>
    );
}

export default Home;
