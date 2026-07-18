import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
  useMapEvents,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

function ClickHandler({ onSelect }) {
  useMapEvents({
    click(e) {
      let { lat, lng } = e.latlng;

      lat = Math.max(-90, Math.min(90, lat));

      lng = ((lng + 180) % 360 + 360) % 360 - 180;

      onSelect({
        lat,
        lng,
      });
    },
  });

  return null;
}

function FlyToLocation({ location }) {
  const map = useMap();

  if (location) {
    map.flyTo([location.lat, location.lng], 8, {
      animate: true,
      duration: 1.5,
    });
  }

  return null;
}

export default function MapView({
  location,
  onSelect,
  hotspots = [],
}) {
  return (
    <MapContainer
      center={[20, 0]}
      zoom={2}
      worldCopyJump={true}
      maxBounds={[
        [-90, -180],
        [90, 180],
      ]}
      maxBoundsViscosity={1}
      scrollWheelZoom={true}
      style={{
        height: "500px",
        width: "100%",
        borderRadius: "16px",
      }}
    >
      <TileLayer
        attribution="© OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <ClickHandler onSelect={onSelect} />

      <FlyToLocation location={location} />

      {location && (
        <Marker position={[location.lat, location.lng]}>
          <Popup>
            <b>Selected Location</b>
            <br />
            Latitude: {location.lat.toFixed(4)}
            <br />
            Longitude: {location.lng.toFixed(4)}
          </Popup>
        </Marker>
      )}

      {hotspots.map((spot, index) => (
        <Marker
          key={index}
          position={[spot.latitude, spot.longitude]}
        >
          <Popup>
            🔥 Fire Hotspot
            <br />
            Confidence: {spot.confidence || "Unknown"}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
