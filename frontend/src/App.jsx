import { useState } from "react";
import MapView from "./components/MapView";
import Loading from "./components/Loading";
import EcosystemCard from "./components/EcosystemCard";
import { analyzeLocation } from "./services/api";

function App() {
  const [location, setLocation] = useState({
    lat: 10.0159,
    lng: 76.3419,
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const analyze = async () => {
    if (loading) return;

    setLoading(true);
    setError("");

    try {
      const data = await analyzeLocation(location.lat, location.lng);
      setResult(data);
    } catch (err) {
      setError("Unable to analyze location.");
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>🌍 PlanetIQ</h1>
      <p>AI Powered Ecosystem Intelligence</p>

      <MapView
        location={location}
        setLocation={setLocation}
      />

      <h3>
        Selected:
        {" "}
        {location.lat.toFixed(4)}
        ,
        {" "}
        {location.lng.toFixed(4)}
      </h3>

      <button
        onClick={analyze}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze Location"}
      </button>

      {loading && <Loading />}

      {error && (
        <p style={{ color: "red" }}>{error}</p>
      )}

      {result && (
        <EcosystemCard data={result} />
      )}
    </div>
  );
}

export default App;
