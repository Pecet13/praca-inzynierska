import { useState, useEffect } from "react";
import api from "../api";
import placeholder from "../assets/placeholder.png";
import { Link } from "react-router-dom";
import "../styles/Ranking.css";

function Ranking() {
    const [productTypes, setProductTypes] = useState([]);
    const [productType, setProductType] = useState(0);
    const [rankings, setRankings] = useState([]);
    const [categories, setCategories] = useState([]);
    const [category, setCategory] = useState(1);
    const [reverse, setReverse] = useState(false);

    useEffect(() => {
        getProductsTypes();
        getRankings();
        getCategories();
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

    const getRankings = () => {
        api.get("/api/rankings/")
            .then((res) => {
                setRankings(res.data);
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
        setCategory(
            categories.filter((cat) => cat.product_type === productType)[0]
                ?.id || 1
        );
    };

    const base = rankings
        .filter((item) => item.category.id === category)
        .sort((a, b) => a.rank - b.rank);

    let filteredRanking = reverse ? [...base].reverse() : base;

    return (
        <div className="ranking-wrapper">
            <h1 className="h1">Ranking</h1>
            <div className="ranking-select-wrapper">
                <div className="selects">
                    <select
                        className="select"
                        value={productType}
                        onChange={(e) => {
                            setProductType(Number(e.target.value));
                            setCategories(
                                categories.filter(
                                    (cat) =>
                                        cat.product_type.id ===
                                        Number(e.target.value)
                                )
                            );
                            setCategory(categories[0]);
                        }}
                    >
                        {productTypes.map((pt) => (
                            <option key={pt.id} value={pt.id}>
                                {pt.name}
                            </option>
                        ))}
                    </select>
                    <select
                        className="select"
                        value={category}
                        onChange={(e) => setCategory(Number(e.target.value))}
                    >
                        {categories.map((cat) => (
                            <option key={cat.id} value={cat.id}>
                                {cat.name}
                            </option>
                        ))}
                    </select>
                </div>
                <label className="reverse">
                    <span className="reverse-text">Reverse </span>
                    <input
                        type="checkbox"
                        checked={reverse}
                        onChange={(e) => setReverse(e.target.checked)}
                    />
                </label>
            </div>
            <div className="ranking-list">
                {filteredRanking.map((item) => (
                    <div key={item.id} className="product">
                        <div className="product-left">
                            <p className="product-rank">{item.rank}.</p>
                            <div className="product-image-container">
                                <img
                                    className="product-image"
                                    src={
                                        item.product.image_url
                                            ? item.product.image_url
                                            : placeholder
                                    }
                                    alt={item.product.name}
                                />
                            </div>
                            <Link
                                to={`/products/${item.product.id}`}
                                className="product-name"
                            >
                                {item.product.name}
                            </Link>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Ranking;
