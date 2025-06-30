import { useState, useEffect } from "react";
import api from "../api";
import placeholder from "../assets/placeholder.png";
import { Link } from "react-router-dom";

// TODO: reverse order, styling

function Ranking() {
    const [rankings, setRankings] = useState([]);
    const [categories, setCategories] = useState([]);
    const [category, setCategory] = useState(1);

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

    const filteredRanking = rankings.filter(
        (item) => item.category.id === category
    );

    return (
        <div>
            <h1>Ranking</h1>
            <div className="category-selector">
                <select
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
            <div className="product-list">
                {filteredRanking.map((item) => (
                    <div key={item.id} className="product">
                        <div className="product-left">
                            <p className="product-name">{item.rank}.</p>
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
