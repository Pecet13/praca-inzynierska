import "../styles/CustomTooltip.css";

function CustomTooltip({ active, payload, nameX, nameY }) {
    if (active && payload && payload.length) {
        return (
            <div className="custom-tooltip">
                <p>{`Product: ${payload[0].payload.name}`}</p>
                <p>{`${nameX} score: ${payload[0].payload.scoreX}`}</p>
                <p>{`${nameY} score: ${payload[0].payload.scoreY}`}</p>
            </div>
        );
    }
    return null;
}

export default CustomTooltip;
