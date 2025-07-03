import { useState, useEffect } from "react";
import api from "../api";
import placeholder from "../assets/placeholder.png";
import { Link } from "react-router-dom";
import "../styles/Ranking.css";

function Ranking() {
    const [rankings, setRankings] = useState([]);
    const [categories, setCategories] = useState([]);
    const [category, setCategory] = useState(1);
    const [reverse, setReverse] = useState(false);

    useEffect(() => {
        getRankings();
        getCategories();
    }, []);

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
    };

    const base = rankings
        .filter((item) => item.category.id === category)
        .sort((a, b) => a.rank - b.rank);

    let filteredRanking = reverse ? [...base].reverse() : base;

    return (
        <div className="ranking-wrapper">
            <h1 className="h1">Ranking</h1>
            <div className="ranking-select-wrapper">
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
                            <img
                                className="product-image"
                                src={
                                    item.product.image_url
                                        ? item.product.image_url
                                        : placeholder
                                }
                                alt={item.product.name}
                            />
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
