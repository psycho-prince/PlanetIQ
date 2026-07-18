import HealthGauge from "./HealthGauge";

export default function EcosystemCard({ data }) {
  if (!data) return null;

  const weather = data.weather || {};
  const fire = data.fire || {};

  return (
    <div className="card">
      <h2>🌍 Ecosystem Analysis</h2>

      <HealthGauge value={data.ecosystem_health ?? 0} />

      <div className="weather-grid">
        <div className="weather-item">
          <h3>🌡 Temperature</h3>
          <p>
            {weather.temperature !== undefined
              ? `${weather.temperature} °C`
              : "-- °C"}
          </p>
        </div>

        <div className="weather-item">
          <h3>💧 Humidity</h3>
          <p>
            {weather.humidity !== undefined
              ? `${weather.humidity} %`
              : "-- %"}
          </p>
        </div>

        <div className="weather-item">
          <h3>🌧 Precipitation</h3>
          <p>
            {weather.precipitation !== undefined
              ? `${weather.precipitation} mm`
              : "-- mm"}
          </p>
        </div>

        <div className="weather-item">
          <h3>🌬 Wind Speed</h3>
          <p>
            {weather.wind_speed !== undefined
              ? `${weather.wind_speed} km/h`
              : "-- km/h"}
          </p>
        </div>

        <div className="weather-item">
          <h3>🔥 Fire Hotspots</h3>
          <p>{fire.hotspot_count ?? 0}</p>
        </div>

        <div className="weather-item">
          <h3>⚠ Risk Level</h3>
          <p>{data.risk || "Unknown"}</p>
        </div>
      </div>

      <div className="recommendations">
        <h3>📋 Recommendations</h3>

        <ul>
          {(data.recommendations || []).map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
