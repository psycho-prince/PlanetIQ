import { useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  async function analyze() {
    setLoading(true);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/analyze",
        {
          latitude: 9.9312,
          longitude: 76.2673,
        }
      );

      setData(res.data);
    } catch (err) {
      console.log(err);
      alert("Backend not reachable.");
    }

    setLoading(false);
  }

  return (
    <div
      style={{
        background: "#111827",
        color: "white",
        minHeight: "100vh",
        padding: "30px",
        fontFamily: "Arial",
      }}
    >
      <h1>🌍 PlanetIQ</h1>

      <button
        onClick={analyze}
        style={{
          padding: "12px",
          marginBottom: "20px",
        }}
      >
        {loading ? "Analyzing..." : "Analyze Location"}
      </button>

      {data && (
        <>
          <h2>Ecosystem Health</h2>

          <h1>{data.ecosystem_health}%</h1>

          <h3>Risk</h3>

          <p>{data.risk}</p>

          <h3>Weather</h3>

          <p>
            Temperature:
            {data.weather.data.temperature}°C
          </p>

          <p>
            Humidity:
            {data.weather.data.humidity}%
          </p>

          <p>
            Wind:
            {data.weather.data.wind_speed} km/h
          </p>

          <h3>Recommendation</h3>

          <ul>
            {data.recommendations.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;
