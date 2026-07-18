import { useState } from "react";
import axios from "axios";
import MapView from "./components/MapView";
import "./App.css";

function App() {
  const [location, setLocation] = useState({
    lat: 9.9312,
    lng: 76.2673,
  });

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  async function analyze() {
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/analyze", {
        latitude: location.lat,
        longitude: location.lng,
      });

      setData(res.data);
    } catch (err) {
      console.error(err);
      alert("Cannot connect to backend.");
    }

    setLoading(false);
  }

  return (
    <div
      style={{
        maxWidth: "1100px",
        margin: "30px auto",
        fontFamily: "Arial",
      }}
    >
      <h1>🌍 PlanetIQ</h1>
      <p>AI Powered Ecosystem Intelligence</p>

      <MapView
        location={location}
        onSelect={(pos) => setLocation(pos)}
      />

      <br />

      <button
        onClick={analyze}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze Selected Location"}
      </button>

      <br />
      <br />

      <strong>Latitude:</strong> {location.lat.toFixed(4)}
      <br />
      <strong>Longitude:</strong> {location.lng.toFixed(4)}

      {data && (
        <>
          <hr />

          <h2>Ecosystem Health</h2>
          <h1>{data.ecosystem_health}%</h1>

          <h3>Risk</h3>
          <p>{data.risk}</p>

          <h3>Weather</h3>
          <p>🌡 {data.weather.data.temperature} °C</p>
          <p>💧 {data.weather.data.humidity}%</p>
          <p>🌬 {data.weather.data.wind_speed} km/h</p>

          <h3>Recommendations</h3>
          <ul>
            {data.recommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;
