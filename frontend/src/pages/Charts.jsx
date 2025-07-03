import { useState, useEffect } from "react";
import api from "../api";
import "../styles/Charts.css";

function Charts() {
    const [rankings, setRankings] = useState([]);
    const [categories, setCategories] = useState([]);
    const [categoryX, setCategoryX] = useState(0);
    const [categoryY, setCategoryY] = useState(0);

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

    const rankingX = rankings
        .filter((item) => item.category.id === categoryX)
        .sort((a, b) => a.rank - b.rank);

    const rankingY = rankings
        .filter((item) => item.category.id === categoryY)
        .sort((a, b) => a.rank - b.rank);

    return (
        <div className="charts-wrapper">
            <h1 className="h1">Charts</h1>
            <div className="charts-select-wrapper">
                <div className="select-left">
                    <label htmlFor="select-x" className="select-text">
                        X-Axis
                    </label>
                    <select
                        className="select"
                        id="select-x"
                        value={categoryX}
                        onChange={(e) => setCategoryX(Number(e.target.value))}
                    >
                        <option value="">Select Category</option>
                        {categories.map((cat) => (
                            <option key={cat.id} value={cat.id}>
                                {cat.name}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="select-right">
                    <label htmlFor="select-y" className="select-text">
                        Y-Axis
                    </label>
                    <select
                        className="select"
                        id="select-y"
                        value={categoryY}
                        onChange={(e) => setCategoryY(Number(e.target.value))}
                    >
                        <option value="">Select Category</option>
                        {categories.map((cat) => (
                            <option key={cat.id} value={cat.id}>
                                {cat.name}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
        </div>
    );
}

export default Charts;
