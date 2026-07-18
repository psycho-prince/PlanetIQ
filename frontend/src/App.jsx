import { useState } from "react";
import MapView from "./components/MapView";
import EcosystemCard from "./components/EcosystemCard";
import Loading from "./components/Loading";
import { analyzeLocation } from "./services/api";
import "./dashboard.css";

export default function App() {
  const [location, setLocation] = useState({
    lat: 10.0159,
    lng: 76.3419,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    if (loading) return;

    setLoading(true);
    setError("");

    try {
      const data = await analyzeLocation(
        location.lat,
        location.lng
      );

      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Unable to analyze this location.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">

      <header className="header">
        <h1>🌍 PlanetIQ</h1>
        <p>AI Powered Ecosystem Intelligence</p>
      </header>

      <MapView
        location={location}
        onSelect={(latlng) =>
          setLocation({
            lat: latlng.lat,
            lng: latlng.lng,
          })
        }
      />

      <div className="controls">

        <button
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Selected Location"}
        </button>

        <div className="coords">
          <p>
            <strong>Latitude:</strong>{" "}
            {location.lat.toFixed(4)}
          </p>

          <p>
            <strong>Longitude:</strong>{" "}
            {location.lng.toFixed(4)}
          </p>
        </div>

      </div>

      {loading && <Loading />}

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {result && (
        <EcosystemCard data={result} />
      )}

    </div>
  );
}
