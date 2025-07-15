import { useState, useEffect } from "react";
import api from "../api";
import placeholder from "../assets/placeholder.png";
import { Link } from "react-router-dom";
import "../styles/Ranking.css";

function Ranking() {
    const [productTypes, setProductTypes] = useState([]);
    const [productType, setProductType] = useState(1);
    const [rankings, setRankings] = useState([]);
    const [categories, setCategories] = useState([]);
    const [filteredCategories, setFilteredCategories] = useState([]);
    const [category, setCategory] = useState(0);
    const [aiUsers, setAiUsers] = useState([]);
    const [rankingSource, setRankingSource] = useState(-1);
    const [reverse, setReverse] = useState(false);

    useEffect(() => {
        getProductsTypes();
        getRankings();
        getCategories();
        getAiUsers();
    }, []);

    useEffect(() => {
        const filtered =
            productType === 0
                ? categories
                : categories.filter((cat) => cat.product_type === productType);
        setFilteredCategories(filtered);
        setCategory(filtered[0]?.id || 0);
    }, [productType, categories]);

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
    };

    const getAiUsers = () => {
        api.get("/api/ai-users/")
            .then((res) => {
                setAiUsers(res.data);
            })
            .catch((err) => {
                console.error(err);
            });
    };

    const base = rankings
        .filter(
            (item) =>
                item.category.id === category &&
                (rankingSource !== -1
                    ? item.user !== null && item.user.id === rankingSource
                    : item.user === null)
        )
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
                        {filteredCategories.map((cat) => (
                            <option key={cat.id} value={cat.id}>
                                {cat.name}
                            </option>
                        ))}
                    </select>
                    <select
                        className="select"
                        value={rankingSource}
                        onChange={(e) => {
                            setRankingSource(Number(e.target.value));
                        }}
                    >
                        <option value={-1}>All users</option>
                        {aiUsers.map((user) => (
                            <option key={user.id} value={user.id}>
                                {user.username}
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
