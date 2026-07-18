import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 10000,
});

export async function analyzeLocation(latitude, longitude) {
  const response = await api.post("/analyze", {
    latitude,
    longitude,
  });

  return response.data;
}

export default api;
