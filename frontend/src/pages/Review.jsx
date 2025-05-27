import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/Review.css";
import "../styles/Button.css";

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
        getComparisons();
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

    const getComparisons = () => {
        api.get(`/api/products/${id}/review/`)
            .then((res) => {
                if (res.data.length > 0) {
                    setRows(
                        res.data.map((item) => ({
                            category: item.category.toString(),
                            result: item.result,
                            product2: item.product2.toString(),
                        }))
                    );
                }
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
        console.log("API:", api);
        console.log("api.post:", api?.post);
        console.log("id:", id, "rows:", rows);
        api.post(
            `/api/products/${id}/review/`,
            rows.map((row) => ({
                category: parseInt(row.category, 10),
                product2: parseInt(row.product2, 10),
                result: row.result,
            }))
        )
            .then(() => {
                alert("Review submitted successfully.");
                navigate(-1);
            })
            .catch((err) => {
                console.error(err);
                alert("Error submitting review.");
            });
    };

    const cancel = () => {
        navigate(-1);
    };

    return (
        <div className="review-wrapper">
            <h1>Review for: {productName}</h1>
            <div className="comparison-list">
                {rows.map((row, index) => (
                    <div className="comparison" key={index}>
                        <select
                            className="select"
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
                            className="select"
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
                            className="select"
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
                        {rows.length > 1 && (
                            <button
                                className="button button-remove"
                                type="button"
                                onClick={() => removeRow(index)}
                            >
                                x
                            </button>
                        )}
                    </div>
                ))}
            </div>
            <div className="controls">
                <button
                    className="button button-primary"
                    type="button"
                    onClick={addRow}
                >
                    Add comparison
                </button>
                <div className="confirmation">
                    <button
                        className=" button button-secondary button-full"
                        type="button"
                        onClick={cancel}
                    >
                        Cancel
                    </button>
                    <button
                        className="button button-primary button-full"
                        type="submit"
                        onClick={confirm}
                    >
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Review;
