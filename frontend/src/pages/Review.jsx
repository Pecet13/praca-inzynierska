import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";

function Review() {
    const { id } = useParams();
    const [productName, setProductName] = useState("");
    const [categories, setCategories] = useState([]);
    const [products, setProducts] = useState([]);
    const [rows, setRows] = useState([
        { category: "", result: "Equal", product2: "" },
    ]);
    const navigate = useNavigate();

    useEffect(() => {
        getProductName();
        getCategories();
        getProducts();
    }, [id]);

    const getProductName = () => {
        api.get(`/api/products/${id}/`)
            .then((res) => {
                setProductName(res.data.name);
            })
            .catch((err) => {
                console.error(err);
            });
    };

    const getCategories = () => {
        api.get("/api/categories/")
            .then((res) => {
                setCategories(res.data);
            })
            .catch((err) => {
                console.error(err);
            });
    };

    const getProducts = () => {
        api.get("/api/products/")
            .then((res) => {
                setProducts(res.data.filter((product) => product.id !== +id));
            })
            .catch((err) => {
                console.error(err);
            });
    };

    const addRow = () => {
        setRows([...rows, { category: "", result: "Equal", product2: "" }]);
    };

    const updateRow = (index, field, value) => {
        const newRows = [...rows];
        newRows[index][field] = value;
        setRows(newRows);
    };

    const removeRow = (index) => {
        if (rows.length <= 1) return; // Prevent removing the last row
        const newRows = [...rows];
        newRows.splice(index, 1);
        setRows(newRows);
    };

    const confirm = () => {
        Promise.all(
            rows.map((row) =>
                api.post(`/api/products/${id}/review/`, {
                    category: parseInt(row.category),
                    product2: parseInt(row.product2),
                    result: row.result,
                })
            )
        )
            .then(() => {
                alert("Review submitted successfully.");
                navigate(-1);
            })
            .catch((err) => {
                console.error(err);
                alert("Error submitting review. See console for details.");
            });
    };

    const cancel = () => {
        navigate(-1);
    };

    return (
        <div>
            <h1>Review for: {productName}</h1>
            {rows.map((row, index) => (
                <div key={index}>
                    <select
                        value={row.category}
                        onChange={(e) =>
                            updateRow(index, "category", e.target.value)
                        }
                    >
                        <option value="">Select Category</option>
                        {categories.map((category) => (
                            <option key={category.id} value={category.id}>
                                {category.name}
                            </option>
                        ))}
                    </select>
                    <select
                        value={row.result}
                        onChange={(e) =>
                            updateRow(index, "result", e.target.value)
                        }
                    >
                        <option value="Equal">Equal</option>
                        <option value="More">More</option>
                        <option value="Less">Less</option>
                    </select>
                    <select
                        value={row.product2}
                        onChange={(e) =>
                            updateRow(index, "product2", e.target.value)
                        }
                    >
                        <option value="">Select Product</option>
                        {products.map((product) => (
                            <option key={product.id} value={product.id}>
                                {product.name}
                            </option>
                        ))}
                    </select>
                    <button onClick={() => removeRow(index)}>Remove</button>
                </div>
            ))}
            <button onClick={addRow}>Add comparison</button>
            <button onClick={confirm}>Confirm</button>
            <button onClick={cancel}>Cancel</button>
        </div>
    );
}

export default Review;
