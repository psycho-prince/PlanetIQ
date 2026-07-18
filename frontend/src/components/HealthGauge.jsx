import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

export default function HealthGauge({ value }) {
  return (
    <div style={{ width: 220, margin: "20px auto" }}>
      <CircularProgressbar
        value={value}
        text={`${value}%`}
        styles={buildStyles({
          pathColor:
            value >= 80
              ? "#22c55e"
              : value >= 60
              ? "#facc15"
              : "#ef4444",
          textColor: "#ffffff",
          trailColor: "#374151",
        })}
      />
      <h3 style={{ textAlign: "center", color: "white" }}>
        Ecosystem Health
      </h3>
    </div>
  );
}

