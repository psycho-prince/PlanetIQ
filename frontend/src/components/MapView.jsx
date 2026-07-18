import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function ClickHandler({ onSelect }) {
  useMapEvents({
    click(e) {
      onSelect(e.latlng);
    },
  });

  return null;
}

export default function MapView({ location, onSelect }) {
  return (
    <MapContainer
      center={[20, 0]}
      zoom={2}
      style={{
        height: "450px",
        width: "100%",
        borderRadius: "12px",
      }}
    >
      <TileLayer
        attribution="© OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <ClickHandler onSelect={onSelect} />

      {location && (
        <Marker
          position={[
            location.lat,
            location.lng,
          ]}
        />
      )}
    </MapContainer>
  );
}
