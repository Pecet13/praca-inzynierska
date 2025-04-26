import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

function Product({ product }) {
    const { isLoggedIn } = useContext(AuthContext);

    return (
        <div className="product">
            {/* <img src={product.image_url} alt={product.name} /> */}
            <h2>{product.name}</h2>
            <p>{product.description}</p>
            {isLoggedIn && (
                <div>
                    <button >Add review</button>
                </div>
            )}
        </div>
    );
}

export default Product;
