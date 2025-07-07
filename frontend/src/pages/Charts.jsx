import { useState, useEffect } from "react";
import api from "../api";
import {
    ResponsiveContainer,
    ScatterChart,
    XAxis,
    YAxis,
    CartesianGrid,
    Scatter,
    Label,
    LabelList,
    Tooltip,
} from "recharts";
import CustomTooltip from "../components/CustomTooltip";
import { useNavigate } from "react-router-dom";
import "../styles/Charts.css";

function Charts() {
    const [productTypes, setProductTypes] = useState([]);
    const [productType, setProductType] = useState(1);
    const [rankings, setRankings] = useState([]);
    const [products, setProducts] = useState([]);
    const [categories, setCategories] = useState([]);
    const [filteredCategories, setFilteredCategories] = useState([]);
    const [categoryX, setCategoryX] = useState(0);
    const [categoryY, setCategoryY] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        getProductsTypes();
        getRankings();
        getCategories();
        getProducts();
    }, []);

    useEffect(() => {
        const filtered =
            productType === 0
                ? categories
                : categories.filter((cat) => cat.product_type === productType);
        setFilteredCategories(filtered);
        setCategoryX(filtered[0]?.id || 0);
        setCategoryY(filtered[0]?.id || 0);
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

    const getProducts = () => {
        api.get("/api/products/")
            .then((res) => {
                setProducts(res.data);
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

    let categoryXName =
        categories.find((cat) => cat.id === categoryX)?.name || "X-Axis";
    let categoryYName =
        categories.find((cat) => cat.id === categoryY)?.name || "Y-Axis";

    const data = products.map((product) => {
        const rankX = rankingX.find((item) => item.product.id === product.id);
        const rankY = rankingY.find((item) => item.product.id === product.id);
        return {
            id: product.id,
            name: product.name,
            scoreX: rankX ? rankX.score : 0,
            scoreY: rankY ? rankY.score : 0,
        };
    });

    return (
        <div className="charts-wrapper">
            <h1 className="h1">Charts</h1>
            <div className="charts-select-wrapper">
                <div className="charts-select-container">
                    <select
                        className="charts-select"
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
                </div>
                <div className="charts-select-container">
                    <label htmlFor="select-x" className="select-text">
                        X-Axis
                    </label>
                    <select
                        className="charts-select"
                        id="select-x"
                        value={categoryX}
                        onChange={(e) => setCategoryX(Number(e.target.value))}
                    >
                        {filteredCategories.map((cat) => (
                            <option key={cat.id} value={cat.id}>
                                {cat.name}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="charts-select-container">
                    <label htmlFor="select-y" className="select-text">
                        Y-Axis
                    </label>
                    <select
                        className="charts-select"
                        id="select-y"
                        value={categoryY}
                        onChange={(e) => setCategoryY(Number(e.target.value))}
                    >
                        {filteredCategories.map((cat) => (
                            <option key={cat.id} value={cat.id}>
                                {cat.name}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
            <ResponsiveContainer width="75%" height={600}>
                <ScatterChart
                    margin={{
                        top: 50,
                        right: 50,
                        bottom: 50,
                        left: 50,
                    }}
                >
                    <CartesianGrid />
                    <XAxis
                        dataKey="scoreX"
                        type="number"
                        domain={["dataMin", "dataMax"]}
                        name={categoryXName}
                    >
                        <Label
                            value={categoryXName}
                            position="bottom"
                            dy={-10}
                            style={{ fontSize: "1.5rem" }}
                        />
                    </XAxis>
                    <YAxis
                        dataKey="scoreY"
                        type="number"
                        domain={["dataMin", "dataMax"]}
                        name={categoryYName}
                    >
                        <Label
                            value={categoryYName}
                            position="center"
                            dx={-15}
                            angle={-90}
                            style={{ fontSize: "1.5rem" }}
                        />
                    </YAxis>
                    <Scatter
                        data={data}
                        fill="#8884d8"
                        cursor={"pointer"}
                        onClick={(e) => {
                            navigate(`/products/${e.id}`);
                        }}
                    >
                        <LabelList dataKey="name" position="top" />
                    </Scatter>
                    <Tooltip
                        content={(props) => (
                            <CustomTooltip
                                {...props}
                                nameX={categoryXName}
                                nameY={categoryYName}
                            />
                        )}
                    />
                </ScatterChart>
            </ResponsiveContainer>
        </div>
    );
}

export default Charts;
